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
	buf := new(bytes.Buffer)
	var err error
	//width := 6576
	//height := 4384
	//depth := 3
	size := 86487552//width * height * depth
	buf.Grow(size)

	//rand_data := "/dev/shm/shmlab/foo.bin"

	fmt.Printf("Start: %s\n", time.Now().String())
	for i := 0; i < size; i++ {
		myval := fastrand.Uint32()
		err = binary.Write(buf, binary.LittleEndian, myval)
		check(err)
	}
	fmt.Printf("Buffd: %s\n", time.Now().String())


	fpath := "/dev/shm/shmlab/foo.bin"
	err = os.MkdirAll(filepath.Dir(fpath), os.ModePerm)
	check(err)
	elapsed := TimedWriteToFile(fpath, buf)
	npb := int(elapsed.Nanoseconds()) * 1024 / buf.Len()
	log.Printf("Write took %s (%d ns/KiB)\n", elapsed, npb)

	elapsed = TimedReadFile(fpath)
	npb = int(elapsed.Nanoseconds()) * 1024 / buf.Len()

	log.Printf("Read  took %s (%d ns/KiB)\n", elapsed, npb)
	check(os.Remove(fpath))
	fmt.Printf("Done : %s\n", time.Now().String())


}
