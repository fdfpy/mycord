<?php


//system("pwd");
//system("whoami");
header('Content-Type: text/html; charset=UTF-8');

$today = date("Y-m-d");
echo date("Y")."2";
//$target_day = "2018/5/12";


$yobi=date('w');
echo "yobi";
echo $yobi;

$status="zen";
$flag=0;

$a=$_POST['S_NUM'];
$b=$_POST['COMPANY'];
$c=$_POST['BUY_VALS'];
$d=$_POST['KESSAN'];
$e=$_POST['PRE_HITOKABUEKI'];
//$f=$_POST['HON_HITOKABUEKI'];
//$g=$_POST['HONKESSAN_MONTH'];
$f=0;
$g=4;


$del=$_POST['DEL'];
$dict=$_POST['DICT'];
$IKKATSU=$_POST['IKKATSU'];
$REVISED=$_POST['REVISED'];
$cyusyutsu=$_POST['CYUSYUTSU'];
$stockreg=$_POST['stockreg']; 




$status=$_POST['status'];
if($status==""){
    $status="zen";
}


echo "stockreg";
echo $stockreg;
echo " // ";

echo "cyusyutsu";
echo $cyusyutsu[0];
//echo $del[0];
//echo "DICT";
//echo $dict[0];
//echo "IKKATSU";
//echo $IKKATSU;
echo "REVISED";
echo $REVISD[0];
echo "STATUS//";
echo $status;


$cnt=count($del);
$i=0;
while ($i<$cnt){
$moji=$moji.$del[$i].',';
$i++;
}

$cntj=count($cyusyutsu);
$j=0;
while ($j<$cntj-1){
$cyu=$cyu.$cyusyutsu[$j].',';
$j++;
}
$cyu=$cyu.$cyusyutsu[$cntj-1];

echo "cyu";
echo $cyu;
echo "///";


//flag=0 銘柄登録 & 詳細表示を実施する。
//flag=1 銘柄入力エラー
//flag=2 選択銘柄を削除
//flag=3 一括更新を実施する。
//flag=4 単一銘柄の更新を実施する

if (is_numeric($a)==FALSE){
$flag=1;
$mes1="[入力形式エラー] 銘柄が数値ではありません";
}
if(  (is_string($b)==FALSE)  || empty($b)==TRUE){
$flag=1;
$mes2="[入力形式エラー] 銘柄名が文字ではありません";
}


if (empty($del)==FALSE){
$flag=2;
}

if ($IKKATSU==1){
$flag=3;

}

if (empty($REVISED[0])==FALSE){
$flag=4;
    }
   
if (empty($cyusyutsu)==FALSE and empty($REVISED[0])==TRUE and $IKKATSU==0 and empty($del)==TRUE){
$flag=5;
    }

if ($stockreg=="read"){
    $flag=6; 
        }





if($status=="zen"){
$zen_html='selected';
$bubun_html='';
}else if($status=="bubun")
{
$zen_html='';
$bubun_html='selected';

}


echo "FLAG";
echo $flag;
//echo "PYTHON/";
//echo $moji;

if($flag==0){
    //system("python /home/pi/Desktop/stock/sqltest.py $a $b $c $d");
    system("python /home/pi/Desktop/stock/sqltest.py $a $b $c $d $e $f $g");
    }elseif($flag==2){
    system("python /home/pi/Desktop/stock/sqldel.py $moji");      
    }elseif($flag==3){
    system("sudo MPLBACKEND=Agg python3 /home/pi/Desktop/stock/stockgetall.py");
    //system("sudo python /home/pi/Desktop/stock/stockgetall.py");    
    }elseif($flag==4){
    system("sudo MPLBACKEND=Agg python3 /home/pi/Desktop/stock/stockget.py $REVISED[0]");
    //system("sudo python /home/pi/Desktop/stock/stockget.py $REVISED[0]");
    }elseif($flag==5){

    system("sudo python /home/pi/Desktop/stock/sqlcyu.py $cyu");

        //system("sudo python /home/pi/Desktop/stock/stockget.py $REVISED[0]");
    }elseif($flag==6){

    system("sudo python /home/pi/Desktop/stock/sqlread.py $a");
    
    $fn0 = '/home/pi/Desktop/stock/read.csv';
    $csvline = file($fn0);
    //echo "csvline";   
    //echo $csvline[0];  
    $stockinfo = split(",",$csvline[0]); 
    //echo "stockinfo";   
    //echo $stockinfo;
    $a=$stockinfo[0];
    $b=$stockinfo[1];
    $c=$stockinfo[2];
    $d=$stockinfo[5];
    $pre_hitokabueki=$stockinfo[10];


    //echo "/aa/";
    //echo $a;


    
            //system("sudo python /home/pi/Desktop/stock/stockget.py $REVISED[0]");
     }





//echo ("<input type="text" name="S_NUM" size="10" value="$a">");




if ($status=="zen"){

$fn = '/home/pi/Desktop/stock/stockdata.csv'; //�f�[�^�t�@�C����

}else if($status=="bubun"){

    $fn = '/home/pi/Desktop/stock/stockdatacyu.csv';   
}


//$fn = '/home/pi/Desktop/stock/sqltest.csv'; //�f�[�^�t�@�C����
$line = file($fn);

//echo $line;
for ($i = 0; $i < count($line); $i++) {
     $data = split(",",$line[$i]); //�^�u���؂� "\t"�@�@�J���}���؂� ","
     #$num_s[$i]=$data[0];
     #$nam_s[$i]=$data[1];
     #$val_s[$i]=$data[2]; 
     #$sig_s[$i]=$data[3];
 };


/* 表示用サンプルデータ */
$itemArray = array(
    '証券番号',
    '銘柄名   一括更新',
    '更新',
    '削除',
    '詳細',
    'rank',
    '決算',
    '2W前',
    '1W前',
    '本日',
    '抽出'
   );
 /*  <select name="data"><option value="1">aaa</option><option value="2">bbb</option><option value="3">ccc</option> */
/*== 変数の設定 ================*/
/*"<select name="status"><option value="zenhyoji">全表示</option><option value="botiboti">部分抽出</option></select>";*/
/*==== 表組の生成 ================*/
/* アイテムの総数 */
$itemNum = count($itemArray);
/* 1行あたりの列の数 */
$cols = 6;
/*行数を割り出し */
$rows = count($line);
/* 変数 $html の初期化 */
$html = "";
/*==== 表組の生成 ================*/

$html .= '<form name="form2" method="post">';

$html .= '<select name="status"><option value="zen"' .$zen_html. '>全表示</option><option value="bubun"' .$bubun_html. '>部分抽出</option></select>';

$html .= "<table border=\"1\">\n";


$html .= "<tr>\n";


//$today = date("Y/m/d");
//echo date("Y")."2";
//$target_day = "2018/5/12";
//if(strtotime($today) -strtotime($target_day)==0){
//  echo "ターゲット日付は今日です";
//}else if(strtotime($today) > strtotime($target_day)){
//  echo "ターゲット日付は過去です";
//}else{
//  echo "ターゲット日付は未来です";
//}


$html .= "<td>".$itemArray[0]."</td> <td>".$itemArray[1].'<input type="checkbox" name="IKKATSU" value=1>'."</td><td>".$itemArray[2]."</td><td>".$itemArray[3]."</td><td>".$itemArray[4]."</td><td>".$itemArray[5]."</td><td>".$itemArray[6]."</td><td>".$itemArray[7]."</td><td>".$itemArray[8]."</td><td>".$itemArray[9]."</td><td>".$itemArray[10]."</td>";
    $html .= "</tr>\n";





//部分抽出する銘柄の銘柄番号を$cyumatに入れる。

$fc = '/home/pi/Desktop/stock/stockdatacyu.csv'; 
$linec = file($fc);

//echo " linec ";
//echo count($linec);//
//echo " ";

for($j=0 ; $j<count($linec) ; $j++){
$cyumat[$j] = split(",",$linec[$j]);
}

echo " cyumat ";
echo $cyumat[1][0];
echo " ";












//決算警告　警告決算前に赤で表示、決算後は黄色で表示するコード
$j=0;
for ($k = 0; $k < count($line); $k++) {
     $data = split(",",$line[$k]); //�^�u���؂� "\t"�@�@�J���}���؂� ","
     $target_day= date("Y")."/".$data[5];


     if(strtotime($target_day)==""){
        $iro='</td><td>';
     }else{

     if(((strtotime($today) -strtotime($target_day))>-7*86400) and  (strtotime($today)<strtotime($target_day))){
       $iro='</td><td bgcolor=yellow>';
     }else if((strtotime($today)-strtotime($target_day))==0){

        $iro='</td><td bgcolor=red>';
     }else if(        ((strtotime($today) - strtotime($target_day))<5*86400) and ((strtotime($today)>strtotime($target_day)))          ){
        $iro='</td><td bgcolor=blue>';
     }else{
        $iro='</td><td>';
    }
    }


//部分抽出する銘柄番号であれば、checkedをいれる
if ($data[0]==$cyumat[$j][0]){

  //echo " data ";
  //echo $data[0];
  //echo " cyumat ";
  //echo $cyumat[$j][0];

  $chked='checked';
  $j=$j+1;
  ///echo " cyumat ";
  //echo $cyumat[$j][0];



}else{
   //echo " ";
   //echo $k;
   //echo " " ;
   //echo $data[0];
    $chked='';
}


//$test_num=kairi_deg($data[14],$data[15],$data[8]);

//echo '/max/';
//echo $data[14];
//echo '/min/';
//echo $data[15];
//echo '/kabuka/';
//echo $data[8];

//echo '/rank/';
//echo $data[17];
//echo '/gettype/';
//echo gettype((int)$data[17]);



//echo '/test_num0/';
//echo $test_num[0];
//echo '/test_num1/';
//echo $test_num[1];

//25日移動平均との乖離ランク, rank=0,1には着色する

//$irokairi= '';

$rank=(int)$data[17]; //string -> integer


    if( $rank==0 ){
      
        $irokairi= '<td bgcolor=#00ff00>';
    }
    elseif( $rank==1 ){
        $irokairi= '<td bgcolor=#ffffcc>';  
    }
    elseif($rank==2){
        $irokairi= '<td>';
 
    }
    elseif($rank==3){
        $irokairi= '<td>';
    
    }

//2W連続5円以上の上昇 ->緑 , 2W連続5円以上の減少 ->赤

$TH=4;

if(($data[6]>$TH) and ($data[7]>$TH)){
    $iro1='</a></td><td bgcolor=green>';
    $ucount++;
}else if(($data[6]<-$TH) and ($data[7]<-$TH)){
    $iro1='</a></td><td bgcolor=red>';
    $dcount++;
}else{
    $iro1='</a></td><td>';
}


//株価が前日より下がった。 ->緑 , 株価が前日より上がった。 ->赤

if( $data[8]-$data[18]< 0 ){
    $iro2='<b><font color="green">';
}else if($data[8]-$data[18] > 0  ){
    $iro2='<b><font color="red">';
}else{
    $iro2='';
}


                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                               //$iro2='</a></td><td bgcolor=green>';
//$html .=  '<td><a href="'.$data[2].'" target="_blank">'.$data[0].$iro1.$data[1].'</td><td>'.'<input type="checkbox" name="REVISED[]" value='.$data[0].'>'.'</td><td>'.'<input type="checkbox" name="DEL[]" value='.$data[0].'>'.'<td>'.'<input type="checkbox" name="DICT[]" value='.$data[0].'>'.'</td><td>'.round($data[3],2).$iro.$data[5].'</td><td>'.$data[6].'</td><td>'.$data[7].'</td><td>'.$data[8].'</td><td>'.$data[9].'</td>';

    $html .=  '<td><a href="'.$data[2].'" target="_blank">'.$data[0].$iro1.$data[1].'</td><td>'.'<input type="checkbox" name="REVISED[]" value='.$data[0].'>'.'</td><td>'.'<input type="checkbox" name="DEL[]" value='.$data[0].'>'.'<td>'.'<input type="checkbox" name="DICT[]" value='.$data[0].'>'.'</td>'.$irokairi.round($data[17],1).$iro.$data[5].'</td><td>'.$data[6].'</td><td>'.$data[7].'</td><td>'.$data[8].'<br>'.$iro2.'('. ($data[8]-$data[18]) .')'.'</font></b>'.'</td><td>'.'<input type="checkbox" name="CYUSYUTSU[]" value='.$data[0].' '.$chked. '>'.'</td>';
  //$html .=  '<td><a href="'.$data[2].'" target="_blank">'.$data[0].$iro1.$data[1].'</td><td>'.'<input type="checkbox" name="REVISED[]" value='.$data[0].'>'.'</td><td>'.'<input type="checkbox" name="DEL[]" value='.$data[0].'>'.'<td>'.'<input type="checkbox" name="DICT[]" value='.$data[0].'>'.'</td><td>'.round($data[17],1).$iro.$data[5].'</td><td>'.$data[6].'</td><td>'.$data[7].'</td><td>'.$data[8].'</td><td>'.'<input type="checkbox" name="CYUSYUTSU[]" value='.$data[0].' '.$chked. '>'.'</td>';
    

    $html .= "</tr>\n";

 };


 if($yobi==6 or $yobi==0 ){
echo "today is holiday";

 }else{
 echo "ucount-dcount//";
 echo $ucount-$dcount;
 $difc= $ucount-$dcount;
 system("sudo python /home/pi/Desktop/stock/sqlcount.py $today $difc");
 }

$html .= '</table><br><input type="submit" value="削除 or 表示">';
$html .= '</form>';







#echo $html_com;

#  for($t = 0; $t < $cols; $t++){
#      $html .= "<td>".$data[$t]."</td>\n";
#  }







?>






<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width">
<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<style>
	svg {width: 5px; height: 5px; border: 1px solid black;}
	.mark { fill: red; stroke: none; }
</style>
<link rel="stylesheet" type="text/css" href="style.css" />

</head>
<title>Stock Investing Tool</title>
<script type="text/javascript" src=""></script>
 
<body>
 
<div class=page>
 
    <h1>
        <a href="/">
            <img class="logo_stock" src="logo.png" alt="Stock">
            <span class="title"><strong class="pi">Pi</strong></span>
        </a><a>Stock Investing Tool</a>
    </h1>
 
 
    <div class=metanav>
 
    </div>

<?= $mes1 ?>
<br>
<?= $mes2 ?>
<br>
<?= $mes3 ?>

<h6>指標リンク</h6>
<br>
<a href="http://www.nippon-num.com/economy/watcher.html" target="_blank">景気ウォッチャー調査</a>
<br>
<a href="https://info.finance.yahoo.co.jp/fx/marketcalendar/detail/7172" target="_blank">鉱工業生産指数</a>
<br>
<a href="https://www.asset-alive.com/nikkei/demand_supply.php" target="_blank">外国人売買動向</a>

<br>
<br>
暴落したときにチェックする指標
<br>
<br>
<a href="https://jp.investing.com/rates-bonds/u.s.-10-year-bond-yield" target="_blank">アメリカ １０年 債券利回り</a>
<br>
<a href="https://chartpark.com/gold.html" target="_blank">アメリカ 金　価格</a>
<br>
<a href="https://www.tradingview.com/symbols/NYMEX-CL1!/?utm_campaign=market_quotes&utm_medium=widget&utm_source=chartpark.com" target="_blank">WTI　原油</a>
<br>
<a href="https://fx.minkabu.jp/indicators/US-CPI" target="_blank">アメリカ CPI</a>




<br>
<br>



<h6>銘柄登録</h6>

<a href="#1">テクニカル分析結果に移動</a>
<form name="form1" method="post">




<table>
<tr><td>証券番号</td><td>会社名</td><td>四季報URL</td><td>決算</tr>
<td><input type="text" name="S_NUM" size="10" value=<?= $a ?>></td><td><input type="text" name="COMPANY" size="15" value=<?= $b ?>></td><td><input type="text" name="BUY_VALS" size="30" value=<?= $c ?>></td><td><input type="text" name="KESSAN" size="5" value=<?= $d ?>></tr>
<tr><td>一株益</td><td>使用しない</td><td>使用しない</tr>
<tr><td><input type="text" name="PRE_HITOKABUEKI" size="5" value=<?= $pre_hitokabueki ?>></td><td><input type="text" name="HON_HITOKABUEKI" size="5" value=<?= 4 ?>></td><td><input type="text" name="HONKESSAN_MONTH" size="5" value=<?= $hon_hitokabueki ?>></td><td><select name="stockreg"><option value="read" selected>*** 読込 ***</option><option value="reg">*** 登録 ***</option></select></tr>
</table>

<input type="submit" value="実行">
</form>



<h6 id="2">銘柄一覧表</h6>
<?= $today; ?><a href="#1">     テクニカル分析結果に移動</a>
<a href="#3">分析開始に移動</a>









<?= $html ?>
<h5 id="3"></h5>
<?= $html_com1 ?>


<a href="#2">銘柄一覧表TOPに移動</a>


<img src="MEANVOL.png"  width="700" height="700">


<a href="http://www.ullet.com/" target="_blank">企業価値検索サービスUllet</a>

<br>
<br>

<div class="center">

<svg id="myGraph"></svg>
<script src="js/sample.js"></script>

</div>



<br>
<br>







<h6 id="1">テクニカルチャート</h6>

<a href="#2">銘柄一覧表に戻る</a>

<img src="<?= $dict[0] ?>.png"  width="800" height="800">

<h6>銘柄選定ルール</h6>
[1]業績<br>
・営業利益が今後も上昇<br>
・営業利益率10%以上<br><br>
[2]PER<br>
・15以下<br>
・15～30<br><br>
[3]株価チャート<br>
・週足が右肩上がり<br>
・週足の短期、中期、長期がすべて上昇<br><br>
[4]財務<br>
・自己資本比率70%以上<br>
・自己資本比率50～70%は準投資候補とする。<br><br>
[5]その他<br>
・購入金額単元  15万以下

<br>
<br>
<h1>WANT条件</h1>
・過去1年以内に上方修正、増配があった。<br>
・前Qは増収増益だった。<br>
<br>











<ul>


</ul>
 
 
</div>
 
</body>
 
</html>