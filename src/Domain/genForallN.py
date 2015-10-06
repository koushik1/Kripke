#!/usr/bin/env python

import sys
from itertools import permutations
from lperm import *

def writeForallBase(ndims):

  print ""
  print "/******************************************************************"
  print " *  User interface, forall%d()" % ndims
  print " ******************************************************************/"
  print ""

  dim_names = getDimNames(ndims)
    
  args = map(lambda a: "typename T"+a.upper(), dim_names)
  argstr = ", ".join(args)    
  print "    template<typename POLICY, %s, typename BODY>" % argstr
  
  args = map(lambda a: "T%s const &is_%s"%(a.upper(), a), dim_names)
  argstr = ", ".join(args)
  print "    RAJA_INLINE void forall%d(%s, BODY const &body){" % (ndims, argstr)
  
  args = map(lambda a: "T"+a.upper(), dim_names)
  argstr = ", ".join(args)    
  
  args = map(lambda a: "is_"+a, dim_names)
  argstr2 = ", ".join(args)
  print "      typedef typename POLICY::LoopOrder L;"
  print "      forall%d_permute<POLICY, %s, BODY>(L(), %s, body);" % (ndims, argstr, argstr2)
  print "    }"  
  print ""


def writeForallPolicy(ndims):

  print ""
  print "/******************************************************************"
  print " *  Policy base class, forall%d()" % ndims
  print " ******************************************************************/"
  print ""

  dim_names = getDimNames(ndims)

  args = map(lambda a: "typename POL_"+(a.upper()), dim_names)
  argstr = ", ".join(args)
  print "    template<typename LOOP_ORDER, %s>" % argstr
  print "    struct ForallPolicy%d {" % (ndims)
  
  args = map(lambda a: "end_"+a, dim_names)
  argstr = ", ".join(args)
  print "      typedef LOOP_ORDER LoopOrder;"
  for dim in dim_names:
    print "      typedef POL_%s Policy%s;" % (dim.upper(), dim.upper())
  print "    };"
  print ""
  

def writeForallPermutations(ndims):

  dim_names = getDimNames(ndims)
  
  print ""
  print "/******************************************************************"
  print " *  Permutations layer for forall%d()" % ndims
  print " ******************************************************************/"
  print ""
  
    
  # Loop over each permutation specialization
  perms = getDimPerms(dim_names)
  for perm in perms:
    # get enumeration name
    enum = getEnumName(perm)
  
    # print function declaration
    args = map(lambda a: "typename T"+a.upper(), dim_names)
    argstr = ", ".join(args)    
    print "      template<typename POLICY, %s, typename BODY>" % argstr
    
    args = map(lambda a: "T%s const &is_%s"%(a.upper(), a), dim_names)
    argstr = ", ".join(args)    
    print "      RAJA_INLINE void forall%d_permute(%s, %s, BODY const &body){" % (ndims, enum, argstr)    
    
    # Create executor
    args = map(lambda a: "typename POLICY::Policy"+(a.upper()), perm)
    polstr = ", ".join(args)
    args = map(lambda a: "T"+(a.upper()), perm)
    setstr = ", ".join(args)
    print "        Forall%dExecutor<%s, %s> const exec;" % (ndims, polstr, setstr)
    
    # Call executor
    args = map(lambda a: "is_"+a, perm)
    setstr = ", ".join(args)
    args = map(lambda a: "int "+a, perm)
    idxstr = ", ".join(args)
    print "        exec(%s, RAJA_LAMBDA(%s){" % (setstr, idxstr)
    argstr = ", ".join(dim_names)  # NOT PERMUTED!
    print "          body(%s);" % argstr
    print "        });"
    print "      }"
         
    print ""
    

def writeForallExecutor(ndims):

  print ""
  print "/******************************************************************"
  print " *  Default Executor for forall%d()" % ndims
  print " ******************************************************************/"
  print ""

  dim_names = getDimNames(ndims)

  args = map(lambda a: "typename POLICY_"+(a.upper()), dim_names)
  polstr = ", ".join(args)
  args = map(lambda a: "typename T"+(a.upper()), dim_names)
  setstr = ", ".join(args)
  print "    template<%s, %s>" % (polstr, setstr)
  print "    class Forall%dExecutor {" % (ndims)
  print "      public:  "
  
  # Create default executor
  args = map(lambda a: "T%s const &is_%s"%(a.upper(), a), dim_names)
  argstr = ", ".join(args)  
  print "        template<typename BODY>"
  print "        inline void operator()(%s, BODY const &body) const {" % argstr
  print "          RAJA::forall<POLICY_I>(is_i, RAJA_LAMBDA(int i){"
  if ndims == 2:  # 2 dimension termination case:
    print "            RAJA::forall<POLICY_J>(is_j, RAJA_LAMBDA(int j){"
  else: # more than 2 dimensions, we just peel off the outer loop, and call an N-1 executor
    args = map(lambda a: "is_"+a, dim_names[1:])
    setstr = ", ".join(args)
    args = map(lambda a: "int "+a, dim_names[1:])
    idxstr = ", ".join(args)  
    print "            exec(%s, RAJA_LAMBDA(%s){" % (setstr, idxstr)
  
  argstr = ", ".join(dim_names)  
  print "              body(%s);" % argstr
  print "            });"
  print "          });"
  print "        }"
    
  # More than 2 dims: create nested ForallNExecutor  
  if ndims > 2:
    print ""
    args = map(lambda a: "POLICY_"+(a.upper()), dim_names[1:])
    polstr = ", ".join(args)
    args = map(lambda a: "T"+(a.upper()), dim_names[1:])
    argstr = ", ".join(args)
    print "      private:"
    print "        Forall%dExecutor<%s, %s> exec;" % (ndims-1, polstr, argstr)
  print "    };"
  print ""    


def writeForallExecutorOpenMPCollapse(ndims):

  print ""
  print "/******************************************************************"
  print " *  OpenMP Auto-Collapsing Executors for forall%d()" % ndims
  print " ******************************************************************/"
  print ""
  print "#ifdef _OPENMP"
  print ""

  dim_names = getDimNames(ndims)
  
  for depth in range(2,ndims+1):
  
    remainder_ndims = ndims - depth

    polargs = []
    setargs = []
    args =  map(lambda a: "typename POLICY_"+a.upper(), dim_names[depth:])
    args.extend(map(lambda a: "typename T"+a.upper(), dim_names[depth:]))
    argstr = ", ".join(args)   
    print "    // OpenMP Executor with collapse(%d)" % depth
    print "    template<%s>" % argstr
    
    args =  map(lambda a: "RAJA::omp_parallel_for_exec", range(0,depth))
    args.extend(map(lambda a: "POLICY_"+a.upper(), dim_names[depth:]))
    args.extend(map(lambda a: "RAJA::RangeSegment", range(0,depth)))
    args.extend(map(lambda a: "T"+a.upper(), dim_names[depth:]))
    argstr = ", ".join(args)   
    print "    class Forall%dExecutor<%s> {" % (ndims, argstr)
    print "      public:  "
    
    # Create collapse(depth) executor function
    print "        template<typename BODY>"
    
    args = map(lambda a: "RAJA::RangeSegment const &is_"+ a, dim_names[0:depth])
    args.extend(map(lambda a: "T%s const &is_%s"%(a.upper(),a), dim_names[depth:ndims]))
    argstr = ", ".join(args)  
    print "        inline void operator()(%s, BODY const &body) const {" % argstr
#    print "          printf(\"collapse(%d)\\n\");" % depth
    
    # get begin and end indices each collapsed RangeSegment
    for a in dim_names[0:depth]:
      print "          int const %s_start = is_%s.getBegin();" % (a,a)
      print "          int const %s_end   = is_%s.getEnd();" % (a,a)
      print ""
    
    # Generate nested collapsed for loops
    print "#pragma omp parallel for collapse(%d)" % depth
    indent = ""
    for d in dim_names[0:depth]:
      print "          %sfor(int %s = %s_start;%s < %s_end;++ %s){" % (indent, d, d, d, d, d)
      indent += "  "
    
    # No more inner loops, so call the loop body directly
    if remainder_ndims == 0:
      argstr = argstr = ", ".join(dim_names)
      print "          %sbody(%s);" % (indent, argstr)
    
    # Just one inner loop, so issue a RAJA::forall
    elif remainder_ndims == 1:      
      d = dim_names[depth]
      print "          %sRAJA::forall<POLICY_%s>(is_%s, RAJA_LAMBDA(int %s){" % (indent, d.upper(), d, d)
      argstr = argstr = ", ".join(dim_names)
      print "          %s  body(%s);" % (indent, argstr)
      print "          %s});" % (indent)
    
    # More than one inner loop, so call an inner executor
    else:      
      #    exec(is_j, is_k, is_l, RAJA_LAMBDA(int j, int k, int l){
      #      body(i, j, k, l);
      #    });
      
      args = map(lambda a: "is_"+a, dim_names[depth:])
      setstr = ", ".join(args)
      args = map(lambda a: "int "+a, dim_names[depth:])
      argstr = ", ".join(args)      
      print "          %sexec(%s, RAJA_LAMBDA(%s){" % (indent, setstr, argstr)
      argstr = argstr = ", ".join(dim_names)
      print "          %s  body(%s);" % (indent, argstr)
      print "          %s});" % (indent)
    
    # Close out collapsed loops
    argstr = "";
    for d in range(0,depth):
      argstr += "} "
    print "          %s" % argstr
    print "        }"
    
      
    # More than 2 dims: create nested ForallNExecutor
    if remainder_ndims >= 2:
      print ""
      args = map(lambda a: "POLICY_"+(a.upper()), dim_names[depth:])
      polstr = ", ".join(args)
      args = map(lambda a: "T"+(a.upper()), dim_names[depth:])
      argstr = ", ".join(args)
      print "      private:"
      print "        Forall%dExecutor<%s, %s> exec;" % (ndims-depth, polstr, argstr)
    print "    };"
    print ""    
    
  print ""
  print "#endif // _OPENMP"
  print ""

ndims = int(sys.argv[1])


# ACTUAL SCRIPT ENTRY:
print """//AUTOGENERATED BY genForallN.py
  
#ifndef __DOMAIN_FORALL%d_H__
#define __DOMAIN_FORALL%d_H__

#include<RAJA/RAJA.hxx>

""" % (ndims, ndims)


# Create the policy struct so the user can define loop policies
writeForallPolicy(ndims)

# Create the default executor
writeForallExecutor(ndims)

# Create the OpenMP collapse() executors
writeForallExecutorOpenMPCollapse(ndims)

# Create all permutation MUX's 
writeForallPermutations(ndims)

# Dump out the base function that the user calls directly
writeForallBase(ndims)

print """
  
#endif
"""

