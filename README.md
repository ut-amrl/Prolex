The code in `src/share/XML-Schema-learner` orignates from https://github.com/kore/XML-Schema-learner

Stable Artifact Link: https://zenodo.org/records/8423505

# List of Claims
1. Section 6.2 claims that Prolex is able to solve 80% of tasks within the two minute time limit. Additionally, Figure 14a shows the breakdown of time required for tasks across the different environments. This is shown in Step 2 of the evaluation instructions
2. Section 6.2 claims that even for the most complex tasks (by AST size),  68% of them are still able to be completed. This is also further broken down in Figure 14b. This is evaluated in Step 3 of the evaluation instructions.
3. Section 6.2 claims that 81% of the completed programs are solved, meaning that they semantically match the ground truth program. Since this step is done manually, it is not completed in the evaluation instructions. However, if desired, the output programs are produced in the output text files which can be evaluated manually.
4. Section 6.3 claims that Prolex is able to solve: 8% more tasks than the No LLM variant, 19% more tasks than the No Prune variant, 24% more tasks than the Sketch Only variant, 8% more than the No Loop Bounds variant, and the No Sketch variant solved none of the tasks. This and the corresponding Figure 15a is shown in Step 4 of the evaluation instructions.
5. Section 6.4 claims that the CVC5 baseline solves only 18% of the tasks for the Easy environment. This claim and the CVC5 line in Figure 15b is shown in Steps 5 and 6 of the evaluation instructions.
6. Section 6.4 claims that a GPT 3.5 based synthesizer is able to solve 25% of representative tasks when it is given *only* the environment. Moreover, Figure 16a shows how well the synthesizer scales with larger environments. Figure 16b shows how well the synthesizer is able to complete and solve the representative tasks. However, this analysis required many manual steps, such as evaluating the synthesis output and comparing to ground truth programs, and thus is not evaluated in the artifact. 
# Download, Installation, and Sanity Testing
### Downloading
- Artifact with tested with Docker version 24.0.4, however we believe the artifact can run on older versions.
- Download the source code into a new directory.
### Installation
- Once downloaded, navigate to the newly created directory.
- Ensure you have a docker container manager running in another process
	- This can be done by executing `sudo dockerd` in another window
- Execute `./docker_runner.sh` to compile the docker image.
	- This should also run the expected conda setup once the docker image is built. It is expected that the conda environment will be `ns_policies_popl` after this step, however if not execute `source setup.sh` in the `/` directory.
- After the first build of the docker image is complete, if you wish to restart the docker image without rebuilding simply execute: 
`docker run -it --gpus 'all' nsp_popl_docker /bin/bash`
	-	Note: this will still require the conda environment to be setup upon entry, which should happen automatically.
### Sanity Test
- Once setup is complete, you should be in the `/src` directory and the `ns_policies_popl` conda environment should be activated.
- As a sanity test for the installation, run `python Synthethizers/Tests/sanity.py` from the `src` directory.
	- Note: `The specified target token ...` output is expected.
# Evaluation
### Prolex
1. Execute `source data_collection.sh` from the `/src` directory to run Prolex, and it's ablations on all tasks and all environments. **Note: This step may take up to 24 hours to complete.** After completion you may want to copy the generated output files (`GDFSTrue.txt`, `GDFSFalse.txt`, `True.txt`, `False.txt`, `NoSketch.txt`, and `NoLoopBound.txt`) outside of the docker container, to ensure that this step does not have to be repeated. **If one of the above text files was not generated or needs to be rerun**:
	 - `GDFSTrue.txt` can be rerun by running `python Synthesizers/Tests/run_exp.py` with `inf_check = [True]` on line `56`.
	 - `GDFSFalse.txt` can be rerun by running `python Synthesizers/Tests/run_exp.py` with `inf_check = [False]` on line `56`.
	 - `True.txt` can be rerun by running `python Synthesizers/Tests/run_exp_no_llm.py` with `inf_check = [True]` on line `56`.
	 - `False.txt` can be rerun by running `python Synthesizers/Tests/run_exp_no_llm.py` with `inf_check = [False]` on line `56`.
	 - `NoSketch.txt` can be rerun by running  `python Synthesizers/Tests/run_exp_no_sketches.py`.
	 - `NoLoopBound.txt` can be rerun by running  `python Synthesizers/Tests/run_exp_no_loop_bound.py`.
2. Execute `python prolex_env_plots.py` from the `/src` directory to evaluate Claim 1. Given differences in machine capabilities (GPUs, RAM, and less CPU parallelization) we expect approximately as low as 73% of benchmarks to be completed in the two minute timeout.
3. Execute `python prolex_ast_plots.py` from the `/src` directory to evaluate Claim 2. Given differences in machine capabilities (GPUs, RAM, and less CPU parallelization) we expected approximately as low as 58% of the most difficult AST benchmarks to be completed in the two minute timeout.
4. Execute `python prolex_variants_plots.py` from the `/src` directory to evaluate Claim 4. We believe that the differences between the Prolex variants should not differ much from the stated difference in Claim 4.
5. Run `raco pkg install rosette` to install the necessary solver. Execute `python cvc5_data_collection.py` from the `/CVC5` directory to generate the data to evaluate Claim 5. **Note: This step may take up to 90 minutes**.
6. Execute `python cvc5_plots.py` from the `/CVC5` directory to evaluate Claim 5. Given differences in machine capabilities (RAM, and less CPU parallelization) we expect approximately as low as 15% of benchmarks to be completed in the two minute timeout.
# Artifact Description
### Directory Structure
>-- Docker and Conda setup scripts and files
>--**CVC5/**: Contains `*.rkt` files which contains the encoded tasks for being solved by the CVC5 solver
>>--`cvc5_data_collection.py` contains the python calls to collect data for all CVC5 encodings.
>>--`cvc5_plots.py` contains the script to evaluate Claim 5.
>
>--**src/**
>>--`dsl.py` contains our DSL definition.
>>--`demo.py` contains the format for demonstrations.
>>--`data_collection.sh` contains the python calls to collect data for all Prolex variants.
>>--`prolex_env_plots.py` contains the script to evaluate Claim 1.
>>--`prolex_ast_plots.py` contains the script to evaluate Claim 2.
>>--`prolex_variants_plots.py` contains the script to evaluate Claim 4.
>>--**data_parsers/**: Contains the scripts to parse the output data generated from running the data collection step.
>>>--`Prolex_NoLLM_data_parser.py` parses data from the NoLLM variant.
>>>--`Prolex_NoLoopBound_data_parser.py` parses data from the NoLoopBound variant.
>>>--`Prolex_NoPrune_data_parser.py` parses data from the NoPrune variant.
>>>--`Prolex_NoSketch_data_parser.py` parses data from the NoSketch variant.
>>>--`Prolex_SketchOnly_data_parser.py` parses data from the SketchOnly variant.
>>>--`Prolex_data_parser.py` parses data from the full Prolex variant.
>>
>>--**share/**: Contains the code for the off-the-shelf XML based Regex learner.
>>--**benchmark/**: Contains environments and tasks used for evaluating Prolex.
>>>**Environments/**: Contains 6 potential base environments that can be randomized with `f.py`. The base environment which is most extensive, and used in the experiments is contained in `E.py`.
>>>**Tasks/**: Contains the set of tasks that are executed by Prolex for the experiments.
>>
>>-- **Env/**: Contains environment class definitions as well as classes for locations, relations, objects, and the robot
>>-- **Synthesizers/**: Contains all aspects of the Prolex synthesizer
>>>-- **Tests/**: Contains the tests used to run the Prolex experiments and ablations.
>>>>`run_exp.py` runs Prolex, as well as the NoPrune variant.
>>>>`run_exp_no_llm.py` runs the Prolex NoLLM and SketchOnly variants.
>>>>`run_exp_no_sketches.py` Runs the NoSketch variant of Prolex.
>>>>`run_exp_no_loop_bound.py` Runs the NoLoopBound variant of Prolex.
>>>>`sanity.py` Runs the build sanity check.
>>>
>>>**Sketch Completion**
>>>-- `parallel_enumeration.py` is the top level code for executing Prolex sketch completion.
>>>--`worklist_sketch_completion.py` is the sketch completion algorithm of Prolex.
>>>--`find_hole.py` is used to find the next hole given a sketch.
>>>--`ordered_hole_fills_w_prob.py` is used to order potential hole fills given a sketch and the hole to be filled.
>>>--`fill_holes.py` returns a new sketch with a selected hole filled, with a selected hole fill.
>>>--`infeasibility_check.py` is used to evaluate whether or not the current sketch is feasible.
>>>--`check.py` is used to evaluate whether a completed program matches the given demonstration.
>>>--`lm_w_prob.py` is used to get the result from the LLM.
>>>--`get_hole_sentence.py` is used by `lm_w_prob.py` to get the context for the LLM.
>>>**Sketch Generation**
>>>--`end_to_end_sketch_set_gen.py` is the top level sketch generation from demonstration algorithm.
>>>--`demo_to_xml.py` converts the given demonstration into a format compatible with the XML based Regex learner.
>>>--`xml_to_regex_tree.py` applies the Regex learner and uses it's output to create an AST of the produced regex.
>>>--`apply_rewrite_rules.py` is used to create additional regex AST using our defined rewrite rules.
>>>--`translate_regex_tree_to_sketch.py` is used to create a sketch from the regex AST.


### Adding additional tasks
To add additional tasks to test Prolex:
1. Create an additional task file in the `src/benchmark/Tasks/` directory following the format of one of the existing benchmark task files, such as `B6.py`.
2. On line `65` of `src/Synthesizers/Tests/run_exp.py` modify `prog_list` to contain your new task. If you want to only run this new task (**recommended for time**) set `prog_list` to only contain your new task e.g. `prog_list = [Your_Task_Name()]`
3. If you want to only run a specific difficulty, modify the `diff_list` on line `54` of `src/Synthesizers/Tests/run_exp.py` to contain one or more of 'e' (easy), 'm' (medium), or 'h' (hard).
4. To run different variants of Prolex follow the steps below:
	- **NoLLM**: run `python Synthesizers/Tests/run_exp_no_llm.py` with the modified `prog_list` and `inf_check = [True]`
	- **NoPrune**: run `python Synthesizers/Tests/run_exp.py` with the modified `prog_list` and `inf_check = [False]`
	- **SketchOnly**: run `python Synthesizers/Tests/run_exp_no_llm.py` with the modified `prog_list` and `inf_check = [False]`
	- **NoSketch**: run `python Synthesizers/Tests/run_exp_no_sketches.py` with the modified `prog_list` and `inf_check = [True]`
	- **NoLoopBound**: run `python Synthesizers/Tests/run_exp_no_loop_bound.py` with the modified `prog_list` and `inf_check = [True]`
