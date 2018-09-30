# PyRunner

Run python scripts safely by utilizing Docker

## Dependencies

* docker

## Functions

### run_file

#### Signature

```python
def run_file(filename, args=None, data=None, timeout=10, debug=False)
```

#### Args

* `filename` - The python file to be run
* `args` (Default `None`) - A list of arguments to be called with the program
* `data` (Default `None`) - A list of paths to be included alongside the program, defaults to no paths
* `timeout` (Default `10`) - Time in seconds for how long the program will run, if it takes longer it will be killed
* `debug` (Default `False`) - Prints out debug info if `True`, defaults to no debug info printed

## To Do

* Allow multiple versions
* Allow other modules to be included

## Known Bugs

* Container stream is not real-time
* Container stream is not printed when timeout occurs
* On rare occasions when execution is killed from an external source, teardown may not succeed

