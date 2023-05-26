# Youtube Playlist Information Retrival

This project is a Python script that allows you to retrieve information about a YouTube playlist. It utilizes web scraping techniques to fetch the necessary data from the YouTube website and provides options to save the data in different formats.

## Installation

1. _Clone the repository:_

   ```bash
   git clone https://github.com/tserediani/youtube_playlist.git
   ```

2. _Change into the project directory:_
   ```bash
   cd youtube_playlist
   ```
3. _Create a virtual environment (optional but recommended):_
   ```bash
   python -m venv env
   ```
4. _Activate the virtual environment:_
   _For Windows:_
   ```bash
   env\Scripts\activate
   ```
   _For Unix or Linux:_
   ```bash
   source env/bin/activate
   ```
5. _Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required dependencies._
   ```bash
   pip install -r requirements.txt
   ```

# Usage

1. _Modify the necessary constants and configurations in constants.py to match your requirements._
2. _Run the main script:_
   ```bash
    python main.py
   ```
   The script will start scraping the youtube webstie and extract playlist information of given BASE_URL. The data will be written to desired FROMAT [XLSX/CSV] in the current directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)
