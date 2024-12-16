#include "gzip_reader.h"

#include <cmath>
#include <utility>
#include <stdlib.h>
#include <istream>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace oomph;

/************************************************************************************
 * @brief
 *
 ************************************************************************************/
enum ExitStatus
{
  Success = 0,
  Failure = 1,
  InvalidGZipFile = 2,
  UnableToOpenFile = 3,
  InvalidArguments = 4
};

// FIXME: Allow file write mode (e.g. "a" instead of "w") for GZipWriter
// /************************************************************************************
//  * @brief
//  *
//  * @tparam _CharT
//  * @tparam _Traits
//  ************************************************************************************/
// class GZipWriter
// {
// public:
//   GZipWriter();

//   explicit GZipWriter(const std::string& filename,
//   std::ios_base::openmode __mode = std::ios_base::out);

//   basic_filebuf<char_type, traits_type>* rdbuf() const;
//   _LIBCPP_INLINE_VISIBILITY
//   bool is_open() const;
// #ifndef _LIBCPP_HAS_NO_GLOBAL_FILESYSTEM_NAMESPACE
//   void open(const char* __s, ios_base::openmode __mode = ios_base::out);
// #ifdef _LIBCPP_HAS_OPEN_WITH_WCHAR
//   void open(const wchar_t* __s, ios_base::openmode __mode = ios_base::out);
// #endif
//   void open(const string& __s, ios_base::openmode __mode = ios_base::out);

// #if _LIBCPP_STD_VER >= 17 && !defined(_LIBCPP_HAS_NO_FILESYSTEM_LIBRARY)
//   _LIBCPP_AVAILABILITY_FILESYSTEM _LIBCPP_INLINE_VISIBILITY void open(
//     const filesystem::path& __p, ios_base::openmode __mode = ios_base::out)
//   {
//     return open(__p.c_str(), __mode);
//   }
// #endif // _LIBCPP_STD_VER >= 17

//   _LIBCPP_INLINE_VISIBILITY
//   void __open(int __fd, ios_base::openmode __mode);
// #endif
//   _LIBCPP_INLINE_VISIBILITY
//   void close();

// private:
//   basic_filebuf<char_type, traits_type> __sb_;
// };

/************************************************************************************
 * @brief
 *
 * @param filename
 * @return std::vector<std::string>
 ************************************************************************************/
std::vector<std::string> gzip_load(const std::string& filename)
{
  GZipReader reader;
  reader.open(filename);
  auto file_contents = std::move(reader.read_all());
  return file_contents;
}

/************************************************************************************
 * @brief
 *
 * @param filename
 * @return std::vector<std::string>
 ************************************************************************************/
std::vector<std::string> file_load(const std::string& filename)
{
  std::string line;
  std::vector<std::string> file_data;
  std::ifstream file(filename);
  while (std::getline(file, line))
  {
    file_data.push_back(line);
  }
  file.close();
  return file_data;
}

/************************************************************************************
 * @brief
 *
 * @return int
 ************************************************************************************/
int main(int argc, char** argv)
{
  if (argc != 3)
  {
    std::cout << "\n      *********   ERROR   **********\n"
              << "\nMust specify 2 or 3 keywords on the command line."
              << "You have specified " << argc << "\n   Proper usage:  "
              << "\n         gzip_parser [gzipped_file] [uncompressed_file]\n"
              << "\n      *********  PROGRAM TERMINATING   ***********"
              << "\n   [FAILED] " << std::endl;
    exit(ExitStatus::InvalidArguments);
  }

  // Filenames
  std::string gzip_file{argv[1]};
  std::string uncompressed_file{argv[2]};

  // Load file
  std::vector<std::string> gzip_data = std::move(gzip_load(gzip_file));
  std::vector<std::string> uncompressed_data =
    std::move(file_load(uncompressed_file));

  // Check number of lines
  if (gzip_data.size() != uncompressed_data.size())
  {
    std::cerr << "\nDifferent number of lines!"
              << "\nNumber of lines in .gzip file: " << gzip_data.size()
              << "\nNumber of lines in regular file: "
              << uncompressed_data.size() << std::endl;

    std::cout << "LAST GZIP: '" << gzip_data[gzip_data.size() - 2] << "'"
              << std::endl;
    std::cout << "LAST NORMAL: '"
              << uncompressed_data[uncompressed_data.size() - 2] << "'"
              << std::endl;
    exit(ExitStatus::Failure);
  }

  // Compare line by line
  auto n_line = uncompressed_data.size();
  for (unsigned long long i = 0; i < n_line; i++)
  {
    if (gzip_data[i] != uncompressed_data[i])
    {
      std::cerr << "Lines " << i << " DON'T match! '" << gzip_data[i]
                << "' != '" << uncompressed_data[i] << "'" << std::endl;
      exit(ExitStatus::Failure);
    }
  }

  // Done!
  std::cerr << "\nTest passed -- files match!" << std::endl;
  exit(ExitStatus::Success);
}