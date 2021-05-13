# Opdracht: Letterfrequenties
> Recognize Whether The Sentence Is English Or Dutch With An Accuracy Score Of At Least 90%

## Usage Command

OS X & Linux:

```sh
cat testtext.txt | hadopy --mapper "python mapper1.py" --reducer "python reducer1.py" | hadopy --mapper "python mapper2.py" --reducer "python reducer2.py"
```

Windows:

```sh
type testtext.txt | hadopy --mapper "python mapper1.py" --reducer "python reducer1.py" | hadopy --mapper "python mapper2.py" --reducer "python reducer2.py"
```

## Usage example
To use it:
- Download the entire code as ZIP or clone it
- Put your text file in it (I use [testtext.txt](https://github.com/DragonKiller952/DIP/blob/master/letterfrequentie%20MapReduce/testtext.txt))
- Use the Usage command For your OS system
  
This will give the amount of counted English and Dutch Sentences  

testtext contains 73 Dutch and 119 Engels Sentences.
Running this will give the following output:  
![](Testresult.png)

## Library Install
Describe how to install all the Libraries

OS X & Linux:
```sh
pip3 install sys
pip3 install hadopy
```

Windows:
```sh
pip install sys
pip install hadopy
```

## Code Buddy
Ruben van Raaij:
[https://github.com/GameModes](github)


## Code Explaination
4 files are used in the following order:
mapper1.py -> reducer1.py -> mapper2.py -> reducer2.py
### mapper.py
- test
