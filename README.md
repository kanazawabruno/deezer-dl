# deezer_dl
Project inspired by [spotify-dl](https://github.com/SathyaBhat/spotify-dl)

Downloads songs from any Deezer URL (Playlist or song).


### How do I get this thing running?

Pre-requisite: You need Python 3+

1. Install using pip 
      `sudo pip3 install deezer_dl` 
  (use `pip` if your distro natively provides Python 3)

2. Create your YouTube API key & fetch the keys from [Google Developer Console](https://console.developers.google.com/apis/api/youtube/overview). Set the key as `YOUTUBE_DEV_KEY` environment variable: 
`export YOUTUBE_DEV_KEY='your-youtube-key'`

3. Run the script using `deezer_dl`. 
   `deezer_dl -u <deezer_url>` 
   
   - `deezer_url` is a link to Deezer's playlist. You can get it from the share music menu. 

4. To retrieve download songs as MP3, you will need to install ffmpeg.
  - Linux users can get them by installing libav-tools by using apt-get (`sudo apt-get install -y libav-tools`) or a package manager which comes with your distro
  - Windows users can download FFMPEG pre-built binaries from [here](http://ffmpeg.zeranoe.com/builds/). Extract the file using [7-zip](http://7-zip.org/) to a foldrer and [add the folder to your PATH environment variable](http://www.wikihow.com/Install-FFmpeg-on-Windows) 
  
5. All songs will be saved in `$HOME/deezer_dl/songs`. Also it will create a database `deezerdl.db` for caching all URL links so is not needed to access Google API to get the correct URL for the same song.

### Credits
 - [SathyaBhat](https://github.com/SathyaBhat) for give me the opportunity to work on [spotify-dl](https://github.com/SathyaBhat/spotify-dl/pull/19) so I had the idea to build this project
 
## TODO
- Tests
- Ability to change the default directory  
- ...

## Issues, Feedback
Feel free to raise any bugs/issues under Github issues. Pull requests are also more than welcome.