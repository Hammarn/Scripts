BEGIN {FS=" "}     #delimiter in

{
for (i=1;i<=NF;i++)
{
 arr[NR,i]=$i;
 if(big <= NF)
  big=NF;
 }
}
 
END {
  for(i=1;i<=big;i++)
   {
    for(j=1;j<=NR;j++)
    {
     printf("%s ",arr[j,i]);  #delimiter out
    }
    printf("\n");
   }
}

#command to transpose file:   awk -f testawkss.awk file1 >file2