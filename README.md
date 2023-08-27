# Multithreaded File Transfer

A Python utility for transferring large files (such as Chia plots) between two computers over a 10 Gigabit network connection.

## Project Description

The main goal of this project is to transfer large files (e.g., Chia plots of 100GB) from one computer to another. In this setup, two computers are connected via 10 Gigabit NICs. To maximize the full bandwidth of the 10 Gigabit link, a multithreaded program was developed to move multiple 100GB files to different hard drives on the receiving computer, since each hard drive can only read/write at 200MB/s.

```ascii
[Computer 1] --[10Gb NIC]--> [Router/Switch] --[10Gb NIC]--> [Computer 2]
[ HDD1 ]    [ HDD2 ]   ...   [ HDDn ]            |                  [ HDD1 ]    [ HDD2 ]   ...   [ HDDn ]
                      |--------------------- Multithreaded Transfer ---------------------|
```

## Features

- **Multithreading**: To optimize the transfer speed and utilize the full bandwidth of the 10 Gigabit connection, multiple threads are used to simultaneously transfer different files to different hard drives on the receiving computer.
- **Large File Transfer**: Specifically designed for transferring large files (100GB or larger) between two computers.

## Requirements

- Windows operating system on both computers.
- Python installed on the receiving computer.
- Robocopy installed on the receiving computer.

## Installation

Clone the repository to the receiving computer.

```
git clone https://github.com/yourusername/multithreaded-filetransfer.git
```

## Usage

1. Open the script and edit the following variables to match your system:

- `srcDir`: This is the directory path of the source drive (network shared drive) from where the files will be transferred. For example, if your shared drive is `Z:`, then `srcDir` should be `Z:\\`.
- `destDir0`, `destDir1`, `destDir2`: These are the directory paths of the destination drives on the receiving computer. For example, if your destination drives are `D:`, `E:`, and `F:`, then `destDir0` should be `D:\\`, `destDir1` should be `E:\\`, and `destDir2` should be `F:\\`.

```python
srcDir = "Z:\\"     
destDir0 = "D:\\"   
destDir1 = "E:\\"   
destDir2 = "F:\\"  
```

2. Run the script on the receiving computer.

```
python multithreaded-filetransfer.py
```

### Example output

```
MainThread: 1234567890.123
Active Threads: 5
Z:\: 500 space free
start: 2023-08-28 14:23:45.678901
D:\: 150 space free
E:\: 120 space free
F:\: 200 space free
thread started moving Z:\plot-1234567890.plot
thread started moving Z:\plot-1234567891.plot
Active Threads: 7
end: 2023-08-28 14:23:55.678901
done with Z:\plot-1234567890.plot
done with Z:\plot-1234567891.plot

```
