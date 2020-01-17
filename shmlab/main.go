package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"github.com/valyala/fastrand"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"time"
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

var stopwatch struct {
	last time.Time
	start time.Time
}

func watch_start() {
	stopwatch.start = time.Now()
	stopwatch.last = time.Now()
}

func lap(a ...interface{}) int64 {
	elapsed := time.Since(stopwatch.last)
	now := time.Now()
	stopwatch.last = now
	_, err := fmt.Fprintf(os.Stderr, "%s : %s", now, elapsed)
	_, err = fmt.Fprintln(os.Stderr, a)
	check(err)
	return elapsed.Nanoseconds()
}

func rate(size int64, ns int64, a...interface{}) {
	secs := float64(ns) *1e-9
	fsize := float64(size)
	var unit string
	_rate := fsize / secs
	if _rate > 1e9 {
		unit = "GB"
		_rate = _rate * 1e-9
	} else if _rate > 1e6 {
		unit = "MB"
		_rate = _rate * 1e-6
	} else if _rate > 1e3 {
		unit = "KB"
		_rate = _rate * 1e-3
	} else  {
		unit = "B"
	}
	fmt.Printf("%3.2f %s/s %s\n", _rate, unit, a)
}

// WriteToFile will print any string of text to a file safely by
// checking for errors and syncing at the end.
func TimedWriteToFile(filename string, data *bytes.Buffer) time.Duration {
	start := time.Now()

	err := ioutil.WriteFile(filename, data.Bytes(), 0644)
	check(err)
	elapsed := time.Since(start)
	return elapsed

}// WriteToFile will print any string of text to a file safely by
// checking for errors and syncing at the end.
func TimedReadFile(filename string) time.Duration {
	start := time.Now()

	_, err := ioutil.ReadFile(filename)
	check(err)

	elapsed := time.Since(start)
	return elapsed
}

func main() {
	watch_start()
	var ns int64
	lap()
	buf := new(bytes.Buffer)
	//buf2 := new(bytes.Buffer)
	var err error
	//width := 6576
	//height := 4384
	//depth := 3
	// 86487552
	size := 8648755//width * height * depth
	buf2 := make([]byte, size)
	buf.Grow(size)
	fmt.Println(int64(size), buf.Len(), len(buf2))

	//rand_data := "/dev/shm/shmlab/foo.bin"

	lap("Start")
	for i := 0; i < size; i++ {
		myval := fastrand.Uint32()
		err = binary.Write(buf, binary.LittleEndian, myval)
		check(err)
	}
	lap("Buffed")

	copy(buf2, buf.Bytes())
	ns = lap("copy")
	rate(int64(size), ns, "copy")
	fmt.Println(int64(size), buf.Len(), len(buf2))


	fpath := "/dev/shm/shmlab/foo.bin"
	err = os.MkdirAll(filepath.Dir(fpath), os.ModePerm)
	check(err)

	lap("made file")
	elapsed := TimedWriteToFile(fpath, buf)
	npb := int(elapsed.Nanoseconds()) * 1024 / buf.Len()
	ns = lap("write")
	log.Printf("Write took %s (%d ns/KiB)\n", elapsed, npb)
	rate(int64(buf.Len()), ns, "write")
	fmt.Println("___")

	elapsed = TimedReadFile(fpath)
	npb = int(elapsed.Nanoseconds()) * 1024 / buf.Len()

	ns = lap("read")
	rate(int64(size), ns)
	log.Printf("Read  took %s (%d ns/KiB)\n", elapsed, npb)



	check(os.Remove(fpath))
	fmt.Printf("%s : Done \n", time.Now().String())
	fmt.Println(int64(size), buf.Len(), len(buf2))


}
