# DjBoxDownloader
下载DJ音乐盒上的歌曲

## 记录一下实现流程 ##

1. 打开Fiddler,打来DJ音乐盒官网:[http://www.3378.com.cn/](http://www.3378.com.cn/ "DJ音乐盒"),随便选取一首歌打开,如:
[http://www.3378.com.cn/play/61954.htm](http://www.3378.com.cn/play/61954.htm "柔情无骨美女串烧")
2. 分析页面，查看到如下html元素:
   `<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,28,0" width="500" height="600">`
      `<param name="movie" value="http://webapp.djyule.com/webPlayer.swf?music_ID=61954">`
      `<param name="quality" value="high">`
      `<param name="wmode" value="transparent"> `
      `<embed src="http://webapp.djyule.com/webPlayer.swf?music_ID=61954" quality="high" pluginspage="http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash" width="500" height="600">
    </object>`

从上面可以取得播放器以及ID：[http://webapp.djyule.com/webPlayer.swf?music_ID=61954](http://webapp.djyule.com/webPlayer.swf?music_ID=61954 "播放器")

3. 上一步得到`music_ID=61954`,观察Fiddler获取歌曲信息的是：`http://webapp.djyule.com/dj2010/load_webPlay_musicID.asp?music_ID=61954`返回值为`strLoadMusic=61954,,,柔情无骨美女串烧,,,flash/DJ_64/up090120_1/会员：yesuper lee 柔情无骨美女串烧.mp3,,,1,,,71:02,,,2009-1-21,,,yesuper_lee`

所以可以得出**请求URL信息地址构造(URL1):`http://webapp.djyule.com/dj2010/load_webPlay_musicID.asp?music_ID=音乐ID`**,返回值为`URL1_RESPONSE`
对于上面例子:

    URL1_RESPONSE.split(",,,")[0] = 61954
    URL1_RESPONSE.split(",,,")[1] = 柔情无骨美女串烧`
    URL1_RESPONSE.split(",,,")[2] = flash/DJ_64/up090120_1/会员：yesuper lee 柔情无骨美女串烧.mp3
    URL1_RESPONSE.split(",,,")[3] = 1
    URL1_RESPONSE.split(",,,")[4] = 71:02
    URL1_RESPONSE.split(",,,")[4] = 2009-1-21
    URL1_RESPONSE.split(",,,")[4] = yesuper_lee

**真正歌曲为:`http://a64-1.jyw8.com:8080/up090120_1/会员：yesuper lee 柔情无骨美女串烧.mp3`**

**对比真实地址，可以得出`URL2 = http://a64-1.jyw8.com:8080 + URL1_RESPONSE.split(",,,")[2][len("flash/DJ_64"):]`**

其实还没有完，通过[反编译](http://www.showmycode.com/ "反编译地址")发现如下内容:

    _root.playServerURL1 = "http://a64-1.jyw8.com:8080/";
    _root.playServerURL2 = "http://a64-2.jyw8.com:8080/";
    _root.playServerURL3 = "http://a64-3.jyw8.com:8080/";
    _root.playServerURL4 = "http://a64-4.jyw8.com:8080/";
    _root.playServerURL5 = "http://a64-5.jyw8.com:8080/";
    _root.playServerURL6 = "http://a64-6.jyw8.com:8080/";
    _root.playServerURL7 = "http://a64-7.jyw8.com:8080/";
    _root.playServerURL8 = "http://a64-8.jyw8.com:8080/";
    _root.playServerURL9 = "http://a64-9.jyw8.com:8080/";
    _root.playServerURL10 = "http://a64-10.jyw8.com:8080/";
    _root.playServerURL11 = "http://a64-11.jyw8.com:8080/";
    _root.playServerURL12 = "http://a64-12.jyw8.com:8080/";
    _root.playServerURL13 = "http://a64-13.jyw8.com:8080/";
    _root.playServerURL14 = "http://a64-14.jyw8.com:8080/";
    _root.playServerURL15 = "http://a64-15.jyw8.com:8080/";
    _root.playServerURL16 = "http://a64-16.jyw8.com:8080/";
    _root.playServerURL17 = "http://a64-17.jyw8.com:8080/";
    _root.playServerURL18 = "http://a64-18.jyw8.com:8080/";
    _root.playServerURL19 = "http://a64-19.jyw8.com:8080/";
    _root.playServerURL20 = "http://a64-20.jyw8.com:8080/";

    function starPlayDJ() {
        if ((int(_root.playerMusic_ID) > 97160) && (int(_root.playerMusic_ID) <= 105558)) {
            _root.playerFile = _root.playServerURL2 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 105558) && (int(_root.playerMusic_ID) <= 113933)) {
            _root.playerFile = _root.playServerURL3 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 113933) && (int(_root.playerMusic_ID) <= 123781)) {
            _root.playerFile = _root.playServerURL4 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 123781) && (int(_root.playerMusic_ID) <= 129389)) {
            _root.playerFile = _root.playServerURL5 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 129389) && (int(_root.playerMusic_ID) <= 138471)) {
            _root.playerFile = _root.playServerURL6 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 138471) && (int(_root.playerMusic_ID) <= 144784)) {
            _root.playerFile = _root.playServerURL7 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 144784) && (int(_root.playerMusic_ID) <= 151966)) {
            _root.playerFile = _root.playServerURL8 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 151966) && (int(_root.playerMusic_ID) <= 160431)) {
            _root.playerFile = _root.playServerURL9 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 160431) && (int(_root.playerMusic_ID) <= 167639)) {
            _root.playerFile = _root.playServerURL10 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 167639) && (int(_root.playerMusic_ID) <= 182926)) {
            _root.playerFile = _root.playServerURL11 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 182926) && (int(_root.playerMusic_ID) <= 198890)) {
            _root.playerFile = _root.playServerURL12 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 198890) && (int(_root.playerMusic_ID) <= 213214)) {
            _root.playerFile = _root.playServerURL13 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 213214) && (int(_root.playerMusic_ID) <= 227251)) {
            _root.playerFile = _root.playServerURL14 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 227251) && (int(_root.playerMusic_ID) <= 240890)) {
            _root.playerFile = _root.playServerURL15 + _root.playerFile;
        } else if ((int(_root.playerMusic_ID) > 240890) && (int(_root.playerMusic_ID) <= 268960)) {
            _root.playerFile = _root.playServerURL16 + _root.playerFile;
        } else if (int(_root.playerMusic_ID) > 268960) {
            _root.playerFile = _root.playServerURL17 + _root.playerFile;
        } else {
            _root.playerFile = _root.playServerURL1 + _root.playerFile;
        }
        PlayIndex = MList.selectedIndex;
        _root.saveMList_index = PlayIndex;
        saveMListIndex(PlayIndex);
        _root.R_play_mc.gotoAndPlay("LoadMp3");
    }

所以歌曲下载的服务器地址是根据音乐ID变化的.到此已经可以获取歌曲真实地址了。
