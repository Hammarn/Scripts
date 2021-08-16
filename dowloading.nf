#!/usr/bin/env nextflow

 params.project = "snic2019-8-348"
params.outdir = "dowloaded"
file_list  = Channel.fromPath(params.input)

process dowload {
        publishDir "Results"

        errorStrategy = 'retry'
        
        executor = 'slurm'
        cpus = 1
        time = 24.h
        input:
        file command_file from file_list 

        output:
        file '*' 


        script:
        """
        bash  $command_file
        """

}
