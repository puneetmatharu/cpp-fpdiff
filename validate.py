import os
import shutil
import stat
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Union


def find_hyperfine():
    return shutil.which("hyperfine")


def run(script_path: Union[str, Path], benchmark: bool = False) -> None:
    run_command = f"./{script_path}"
    if benchmark:
        hyperfine_path = find_hyperfine()
        if hyperfine_path is None:
            raise SystemError("Unable to find command 'hyperfine'.")
        print(f"Found hyperfine: {hyperfine_path}")
        run_command = f"{hyperfine_path} --warmup=10 {run_command}"
    print(f"\nRunning: '{run_command}'\n")
    return subprocess.run(run_command, shell=True).returncode


def generate_test_script(executor: str, log_file: str) -> str:
    test_script = f"""
#!/bin/bash
{executor} data/validata/linear_elasticity_simple_prec_results.dat.gz data/Validation/linear_elasticity_simple_prec_results.dat 1.0e-12 0.1 >{log_file}
{executor} data/validata/multi_poisson_simple_prec_results.dat.gz data/Validation/multi_poisson_simple_prec_results.dat >>{log_file}
{executor} data/validata/multi_poisson_two_plus_three_prec_results.dat.gz data/Validation/multi_poisson_two_plus_three_prec_results.dat >>{log_file}
{executor} data/validata/multi_poisson_two_plus_three_upper_triangular_prec_results.dat.gz data/Validation/multi_poisson_two_plus_three_upper_triangular_prec_results.dat >>{log_file}
{executor} data/validata/multi_poisson_two_plus_three_upper_triangular_with_sub_prec_results.dat.gz data/Validation/multi_poisson_two_plus_three_upper_triangular_with_sub_prec_results.dat >>{log_file}
{executor} data/validata/multi_poisson_two_plus_three_upper_triangular_with_two_sub_prec_results.dat.gz data/Validation/multi_poisson_two_plus_three_upper_triangular_with_two_sub_prec_results.dat >>{log_file}
{executor} data/validata/multi_poisson_two_plus_three_upper_triangular_with_replace_prec_results.dat.gz data/Validation/multi_poisson_two_plus_three_upper_triangular_with_replace_prec_results.dat >>{log_file}
{executor} data/validata/multi_poisson_coarse_two_plus_two_plus_one_prec_results.dat.gz data/Validation/multi_poisson_coarse_two_plus_two_plus_one_prec_results.dat >>{log_file}
{executor} data/validata/multi_poisson_one_plus_four_with_two_coarse_results.dat.gz data/Validation/multi_poisson_one_plus_four_with_two_coarse_results.dat >>{log_file}
{executor} data/validata/multi_poisson_upper_triangular_prec_results.dat.gz data/Validation/multi_poisson_upper_triangular_prec_results.dat >>{log_file}
{executor} data/validata/driven_cavity_results.dat.gz data/Validation/driven_cavity_results.dat >>{log_file}
{executor} data/validata/DenseLU_results.dat.gz data/Validation/DenseLU_results.dat >>{log_file}
{executor} data/validata/results_Pe200.dat.gz data/Validation/SuperLU_results.dat >>{log_file}
{executor} data/validata/SuperLU_solve_error.dat.gz data/Validation/SuperLU_solve_error.dat >>{log_file}
{executor} data/validata/results_Pe200.dat.gz data/Validation/GMRES_results.dat >>{log_file}
{executor} data/validata/GMRES_solve_error.dat.gz data/Validation/GMRES_solve_error.dat 0.1 1.0e-12 >>{log_file}
{executor} data/validata/results_Pe200.dat.gz data/Validation/BiCGStab_results.dat >>{log_file}
{executor} data/validata/BiCGStab_solve_error.dat.gz data/Validation/BiCGStab_solve_error.dat 0.1 5.0e-12 >>{log_file}
{executor} data/validata/results_Pe0.dat.gz data/Validation/CG_results.dat >>{log_file}
{executor} data/validata/CG_solve_error.dat.gz data/Validation/CG_solve_error.dat >>{log_file}
{executor} data/validata/results_Pe0.dat.gz data/Validation/GS_results.dat >>{log_file}
{executor} data/validata/GS_solve_error.dat.gz data/Validation/GS_solve_error.dat >>{log_file}
{executor} data/validata/results_Pe0.dat.gz data/Validation/DampedJacobi_results.dat >>{log_file}
{executor} data/validata/DampedJacobi_solve_error.dat.gz data/Validation/DampedJacobi_solve_error.dat >>{log_file}
{executor} data/validata/direct_solver_matrix_solve_result.dat.gz data/Validation/RESLT_DirectSolverTest/DenseLU_DenseDoubleMatrix.dat >>{log_file}
{executor} data/validata/direct_solver_problem_solve_result.dat.gz data/Validation/RESLT_DirectSolverTest/soln0.dat >>{log_file}
{executor} data/validata/direct_solver_problem_solve_result.dat.gz data/Validation/RESLT_DirectSolverTest/soln1.dat >>{log_file}
{executor} data/validata/direct_solver_matrix_solve_result.dat.gz data/Validation/RESLT_DirectSolverTest/SuperLU_CRDoubleMatrix.dat >>{log_file}
{executor} data/validata/direct_solver_matrix_solve_result.dat.gz data/Validation/RESLT_DirectSolverTest/SuperLU_CCDoubleMatrix.dat >>{log_file}
{executor} data/validata/direct_solver_problem_solve_result.dat.gz data/Validation/RESLT_DirectSolverTest/soln2.dat >>{log_file}
    """
    return test_script


def is_python_file(fname: Union[str, Path]) -> bool:
    return True if (Path(fname).suffix == ".py") else False


def parse_args() -> Namespace:
    parser = ArgumentParser("fpdiff comparison tool", 1.0e-01, 1.0e-14)
    parser.add_argument("-e", "--executor", default="fpdiff.py", type=Path)
    parser.add_argument("-o", "--output-file", default="validation.log", type=Path)
    parser.add_argument("-b", "--benchmark", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if not Path(args.executor).exists():
        raise FileNotFoundError(f"Unable to locate executor '{args.executor}'!")

    # Add 'python3' prefix if needed
    executor = f"./{args.executor}"
    if is_python_file(executor):
        executor = f"python3 {executor}"

    # Wipe output file
    if args.output_file.exists():
        args.output_file.unlink()

    # Generate script to run
    script_fpath = "run_script.sh"
    script = generate_test_script(executor=executor, log_file=args.output_file)
    with open(script_fpath, "w") as f:
        f.write(script)

    # Make it executable
    st = os.stat(script_fpath)
    os.chmod(script_fpath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Run
    return_code = run(script_path=script_fpath, benchmark=args.benchmark)
    return return_code


if __name__ == "__main__":
    sys.exit(main())
