from Synthesizers.synthesizer_v0 import *
from Synthesizers.check import *
from dsl import *
import time

env = E1()

t1_demo_e1 = T1_demo_E1()

sketch_max = Prog(1)
i1 = Iterator()
o1 = variable(i1.pretty_str(0))
act1 = Act(None,'Grab')
v = variable(None)
goto1 = Goto('Goto', None)
#act2 = Act_stmnt(None, None, [("On", "Table_0")])
act2 = Act(None, 'Place', [('On', None)])
goto1.add_stmnt(act2)
i2 = Iterator()
l1 = variable(i2.pretty_str(0))
goto2 = Goto('Goto',l1)
goto3 = Goto('Goto_each', itr=i2)
if_s = If(None)
#if_s = If_stmnt(Bexp(None, Check_prop_pred(None, None)))


os = object_set()
sc = Scan(None,os)
for_s = Foreach_obj(i1, os)

if_s.add_stmnt(act1)
goto1.add_stmnt(goto2)
if_s.add_stmnt(goto1)

for_s.add_stmnt(if_s)

goto3.add_stmnt(sc)
goto3.add_stmnt(for_s)
sketch_max.add_stmnt(goto3)

print(sketch_max.pretty_str(1))

sketch_small = Prog(2)
i1 = Iterator()
o1 = variable(i1.pretty_str(0))
act1 = Act(None,'Grab')
v = variable(None)
goto1 = Goto('Goto', None)
table_0 = variable("Table_0")
act2 = Act(None, 'Place', [("On", table_0)])
goto1.add_stmnt(act2)
i2 = Iterator()
l1 = variable(i2.pretty_str(0))
goto2 = Goto('Goto',l1)
goto3 = Goto('Goto_each', itr=i2)
if_s = If(Bexp('neg', Check_prop(None, None)))


os = object_set()
sc = Scan(None,os)
for_s = Foreach_obj(i1, os)

if_s.add_stmnt(act1)
goto1.add_stmnt(goto2)
if_s.add_stmnt(goto1)

for_s.add_stmnt(if_s)

goto3.add_stmnt(sc)
goto3.add_stmnt(for_s)
sketch_small.add_stmnt(goto3)

print(sketch_small.pretty_str(1))

progs = ennumerator_v0(env, sketch_max)

print(len(progs))

print(progs[0].pretty_str(0))

start = time.time()

num_consistent = 0
consistent_prog = []
consistent_found = False
inconsistent_found = False
for i in range(len(progs)):
    if check(t1_demo_e1, progs[i], env, printing=False):
        num_consistent = num_consistent + 1
        if not consistent_found:
            consistent_prog.append(progs[i])
        consistent_found = True

    elif not inconsistent_found:
        inconsistent_prog = progs[i]
        inconsistent_found = False

    if i % 100 == 0:
        cur_time = time.time()
        elap_min = int((cur_time - start)/60)
        elap_sec = int(cur_time-start - 60*elap_min)
        print(str(i) + " MM:" + str(elap_min) + " SS:" + str(elap_sec) + " Consistent: " + str(num_consistent))

cur_time = time.time()
elap_min = int((cur_time - start)/60)
elap_sec = int(cur_time-start - 60*elap_min)
print(str(i) + " MM:" + str(elap_min) + " SS:" + str(elap_sec) + " Consistent: " + str(num_consistent))

print("Number of Completions: " + str(len(progs)))

print(consistent_prog[0].pretty_str(0))