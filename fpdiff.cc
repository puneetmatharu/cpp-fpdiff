#include "fpdiff.h"

/************************************************************************************
 * @brief
 *
 * @return int
 ************************************************************************************/
int main(int argc, char** argv)
{
  if (argc >= 3 && argc <= 5)
  {
    // Set the defaults
    // Max relative difference in percent
    double relative_error_tolerance{1.0e-01};

    // A small number -- essentially round-off error
    double round_off_tolerance{1.0e-14};

    // Read any optional arguments
    if (argc >= 4)
    {
      relative_error_tolerance = std::stod(argv[3]);
      if (argc == 5)
      {
        round_off_tolerance = std::stod(argv[4]);
      }
    } // if (argc >= 4)

    fpdiff(argv[1],
           argv[2],
           relative_error_tolerance,
           round_off_tolerance,
           std::cout);
  }
  else
  {
    std::cout
      << "\n      *********   ERROR   **********\n"
      << "\nMust specify 2, 3 or 4 keywords on the command line."
      << "You have specified " << argc << "\n   Proper usage:  "
      << "\n         fpdiff file1 file2 [max_rel_diff_percent] [small]\n"
      << "\n      *********  PROGRAM TERMINATING   ***********"
      << "\n   [FAILED] " << std::endl;
    exit(4);
    return ExitStatus::InvalidArguments;
  }
}