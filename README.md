# DjBoxDownloader
下载DJ音乐盒上的歌曲

## 记录一下实现流程 ##

1. 打开Fiddler,打来DJ音乐盒官网:[http://www.djyule.com/](http://www.djyule.com/ "DJ音乐盒"),随便选取一首歌打开,如:
[http://www.djyule.com/DJ/61954.htm](http://www.djyule.com/DJ/61954.htm "柔情无骨美女串烧")
2. 分析页面，查看到如下html元素:
```
<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,28,0" width="500" height="600">
	 <param name="movie" value="http://webapp.djyule.com/webPlayer.swf?strLoadMusic=61954,,,柔情无骨美女串烧,,,flash/DJ_64/up090120_1/会员：yesuper lee 柔情无骨美女串烧.mp3,,,1,,,2908749,,,71:02,,,2009-1-21,,,yesuper_lee">
	      <param name="quality" value="high">
	      <embed src="http://webapp.djyule.com/webPlayer.swf?strLoadMusic=61954,,,柔情无骨美女串烧,,,flash/DJ_64/up090120_1/会员：yesuper lee 柔情无骨美女串烧.mp3,,,1,,,2908749,,,71:02,,,2009-1-21,,,yesuper_lee" quality="high" pluginspage="http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash" width="500" height="600">
</object>
```

3. 根据上一步得到播放器的参数:```strLoadMusic=61954,,,柔情无骨美女串烧,,,flash/DJ_64/up090120_1/会员：yesuper lee 柔情无骨美女串烧.mp3,,,1,,,2908749,,,71:02,,,2009-1-21,,,yesuper_lee```,可以得到相应的参数:
* 音乐id:61954
* 音乐名:柔情无骨美女串烧
* 时长:71:02
* 日期: 2009-1-21
那么```flash/DJ_64/up090120_1/会员：yesuper lee 柔情无骨美女串烧.mp3```看起来像地址？


4. 下面开始提取歌曲真实地址了:
反编译播放器:[http://webapp.djyule.com/webPlayer.swf](http://webapp.djyule.com/webPlayer.swf "播放器"),得到如下内容:
```
    function myMusicList() {
        _root.ifPlayStop = true;
        _root.DJpathReload = false;
        _root.R_play_mc.gotoAndStop("\u505C\u6B62");
        thisData = MList.selectedItem.data;
        _root.LStingGe = thisData;
        var _local2 = new Array();
		//strLoadMusic=132576,,,DJ问情-心痛2011【情感车载慢摇】,,,flash/up20101113-1/DJ问情-心痛2011【情感车载慢摇】.mp3,,,2,,,3446723,,,65:47,,,2010-11-13,,,dj问情
        _local2 = thisData.split(",,,");
        _root.playerFile = _local2[2];//flash/up20101113-1/DJ问情-心痛2011【情感车载慢摇】.mp3
        if (int(_local2[0]) > 97160) {
            _root.DJpath = _root.PlayDJdel2(_local2[2]);
        } else {
            _root.DJpath = _root.PlayDJdel(_local2[2]);
        }
        _root.playerMusic_ID = _local2[0];
        if (_root.playerMusic_ID >= 263755) {
            _root.DJpath = jmfilename(_root.DJpath);
        }
        _root.playerFileName = _local2[1];
        _root.this_up_HYname = _local2[7];
        _root.playerTuiJian = _local2[3];
        _root.music_lookCount = _local2[4];
        _root.down320count = _local2[10];
        _root.vote_haoTing = _local2[8];
        _root.vote_buHao = _local2[9];
        newDJurl(_root.DJpath);
    }

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
```
其中`DJpath`为真实下载地址as代码也很简单，具体可以看播放器反编译代码:`ShowMyCode.com.txt`,反编译地址:[http://www.showmycode.com/](http://www.showmycode.com/ "反编译")
