import sys
import pdb

f=open(sys.argv[1])
lines=f.readlines()
f.close()

pop_dic={}

for i,line in enumerate(lines):
        split=line.split()
        num_snps=(len(split)-6)/2
        if pop_dic.has_key(split[0]):
                pop_dic[split[0]].append(i)
        else:
                pop_dic[split[0]]=[i]


fsample=open('samplesize.txt','w')
fcount=open('counts.txt','w')
fpop=open('pops.txt','w')

for p in pop_dic.keys():
        fpop.write('%s\n' %p)
        fsample.write(' '.join([str(len(pop_dic[p])*2)]*num_snps)+'\n')
        vec=[0]*num_snps
        for i in pop_dic[p]:
                split=lines[i].split()
                for j in range(6,len(split),2):
                        if split[j]=='0':
                                vec[(j-6)/2]+=0
                        elif split[j]=='1':
                                vec[(j-6)/2]+=0
                        elif split[j]=='2':
                                vec[(j-6)/2]+=1
                        if split[j+1]=='0':
                                vec[(j-6)/2]+=0
                        elif split[j+1]=='1':
                                vec[(j-6)/2]+=0
                        elif split[j+1]=='2':
                                vec[(j-6)/2]+=1
        fcount.write(' '.join(map(str,vec))+'\n')

fcount.close()
fpop.close()
fsample.close()
