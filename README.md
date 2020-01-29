# Python deprecation

As soon as you are developing a library, SDK or any other piece of code which is intended to be used by several people or software, you have to worry about how to introduce changes gracefully to your code over time.

The following document shows how to use deprecation in python for different scenarios and parts of your code.

Under `./src` directory you are going to find examples with tests showing how to deprecate and test your deprecations. By running, you can explore how it would behave at runtime. By opening it in your favourite IDE you able to check whether your IDE is supporting you by giving any hints when using deprecated stuff. 

## Throwing deprecation warnings

### Method deprecation

*TODO* 

#### Deprecating method arguments

*TODO*

## Class deprecation

*TODO*

### Deprecating a class method

*TODO*

### Deprecating class variables

*TODO*

### Deprecating enum values

*TODO*

## Module deprecation

*TODO*

### Deprecating variables and constants on module level

*TODO*

## Testing deprecations

*TODO*

## Documenting deprecations

*TODO*

## Maintaining deprecations

*TODO*





# Notes

Python provides a built-in integration between the `logging` module and the `warnings` module to let you do this; just call [`logging.captureWarnings(True)`](https://docs.python.org/library/logging.html#logging.captureWarnings) at the start of your script and all warnings emitted by the `warnings` module will automatically be logged at level `WARNING`.

https://code-examples.net/en/q/926881

---

Python warning control https://docs.python.org/3.5/library/warnings.html

---



