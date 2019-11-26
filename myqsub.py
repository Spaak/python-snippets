# Copyright 2019 Eelke Spaak, Donders Institute, Nijmegen
#
# Use as:
#
# myqsub.qsub('walltime=01:00:00,mem=4gb', 'mymodule', 'myfunction', range(10), power=3)
#
# to execute mymodule.myfunction 10 times with arguments 0-9, and kwarg power=3.
# Multiple arguments are supported (each iterable needs to be of the same length),
# and multiple kwargs as well (kwargs are passed as-is to each job).
#
# Adapt the working directory in the pythoncmd variable to the desired working dir.

import os
import numpy as np

def qsub(reqstring, module, fun, *args, **kwargs):
    nargs = len(args)
    njob = len(args[0])
    
    pythoncmd = 'python'
    for k, thisargs in enumerate(zip(*args)):
        argslist = ','.join([str(x) for x in thisargs])
        pythonscript = 'from {} import {}; kwargs={}; {}({}, **kwargs)'.format(module,
            fun, kwargs, fun, argslist)
        
        # escape the python script so that ' is output correctly by echo
        pythonscript = pythonscript.replace("'", "'\\''")
        pythoncmd = 'cd ~/concon/python; python -c "{}"'.format(pythonscript)
        
        # note the -V which ensures the child job inherits the proper environment
        qsubcmd = 'qsub -V -l {} -N j{}_{}'.format(reqstring, thisargs[0], fun)
        fullcmd = 'echo \'{}\' | {}'.format(pythoncmd, qsubcmd)
        
        # make sure each process gets its own Theano compiledir
        # (not very efficient, but unfortunately necessary)
        # theano_flags = 'compiledir=/tmp/theanocompile-{}'.format(str(round(np.random.rand()*1e9)))
        # fullcmd = 'THEANO_FLAGS=\'{}\'; {}'.format(theano_flags, fullcmd)
        
        os.system(fullcmd)
        #print()
    