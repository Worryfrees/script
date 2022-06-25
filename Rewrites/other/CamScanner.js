/*
CamScanner unlocks pro, Cloud scanning is not available.
QuanX 1.0.0:  [rewrite_local]
^https:\/\/(api|api-cs)\.intsig\.net\/purchase\/cs\/query_property\? url script-response-body https://raw.githubusercontent.com/NobyDa/Script/master/Surge/JS/CamScanner.js

Loon:[Script]
http-response https:\/\/(api|api-cs)\.intsig\.net\/purchase\/cs\/query_property\? script-path=https://raw.githubusercontent.com/Worryfrees/script/main/Rewrites/other/CamScanner.js, requires-body=true, timeout=10, tag=CamScanner unlocks pro

Surge4.0: [Script]
http-response https:\/\/(api|api-cs)\.intsig\.net\/purchase\/cs\/query_property\? requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/NobyDa/Script/master/Surge/JS/CamScanner.js
QX & Q & Surge Mitm = ap*.intsig.net,
*/

let obj = JSON.parse($response.body);
obj = {"data":{"psnl_vip_property":{"expiry":"9915130487"}}};
$done({body: JSON.stringify(obj)});
