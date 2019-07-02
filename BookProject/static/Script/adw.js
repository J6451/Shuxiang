(function() {
	var account,CDomain,uid,sid,wa = "_adwq",
		l = "length",
		w = window,
		na = navigator,
		ud = undefined,
		ln = "location",
		d = document,
		ec = encodeURIComponent,
		e = false,
		ncu = '99999999999999999999',
		
                ef = new Array(new Array("etc_n", "adw_channel"),
                               new Array("etc_s", "adw_source"),
                               new Array("etc_g", "adw_group"),
                               new Array("etc_k", "adw_keyword", "adw_term"),
                               new Array("etc_t", "adw_creative", "adw_content"),
                               new Array("etc_c", "adw_campaign"),
                               new Array("etc_m", "adw_media", "adw_medium"),
                               new Array("etc_x", "adw_attr"),
			       new Array("etc_p"));
        

	function domainurl(at){
		server= ('https:' == location.protocol ? 'https://et.emarbox.com' : 'http://et.emarbox.com');
                return server;
        }

	function hash(d) {
		var a = 1, c = 0, h, o;
		if (d) {
			a = 0;
			for (h = d[l] - 1; h >= 0; h--) {
				o = d.charCodeAt(h);
				a = (a << 6 & 268435455) + o + (o << 14);
				c = a & 266338304;
				a = c != 0 ? a ^ c >> 21 : a;
			};
		}
		return a;
	}
	
	function lensplit(s, n) {
		var l = 0;
		var es = "";
		var a = s.split("");
		for ( var i = 0; i < a.length; i++) {
			if (a[i].charCodeAt(0) < 299) {
				l++;
			} else {
				l += 2;
			}
			es += a[i];
			if (l >= n) {
				break;
			}
		}
		return es;
	};
	
	function jugetime(now){
		var h = now.getHours(), m = now.getMinutes();
		if (h == 1) {
			if(m >= 30 ){
				return true;	
			} else {
				return false;
			}
		} else {
			return false;
		}
	}
	
	var jg = jugetime(new Date());
	
	function mc() {
		var rnd="";
		for(var i=0;i<10;i++){
			rnd+=Math.floor(Math.random()*10);
		}
		return rnd;
	}
	
	var CookiesUtil = function(){
		var i = this;
		i.set = function(name, value, expires, path, domain) {
			if (typeof expires == "undefined") {
				expires = "";
			}
			document.cookie = name + "=" + escape(value)
					+ ((expires) ? "; expires=" + expires.toGMTString() : "")
					+ "; path = /"
					+ ((CDomain) ? ";domain=" + CDomain : "");
		};
		i.get = function(name) {
			var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
			if (arr != null) {
				return unescape(arr[2]);
			}
			return null;
		};
		i.clear = function(name, path, domain) {
			if (this.get(name)) {
				document.cookie = name + "="
						+ ((path) ? "; path=" + path : "; path=/")
						+ ((domain) ? "; domain=" + domain : CDomain)
						+ ";expires=Fri, 02-Jan-1970 00:00:00 GMT";
			}
		};
	};
	
	var ad = new Date();
	ad.setTime(ad.getTime() + (24 * 3600 * 1000 * 365 * 2));

	var c = new CookiesUtil;
	
	var cp = function() {
		var i = this;
		var timestamp = (Date.parse(new Date())) / 1000;
		var domainhash = hash(d.domain);
		
		i.ca = function() {
			if (c.get("_adwp") == null) {
				c.set("_adwp", domainhash + "." + mc() + "." + timestamp + "."
						+ timestamp + "." + timestamp + "." + 1, ad);
				this.ct();e = true;
				this.clh();
				return true;
			}
		};
		
		i.ua = function() {
			if (c.get("_adwp") != null) {
				var aq = c.get("_adwp").split(".");
				c.clear("_adwp");
				c.set("_adwp", aq[0] + "." + aq[1] + "." + aq[2] + "." + aq[4]
						+ "." + timestamp + "."
						+ (parseInt(aq[5]) + parseInt(1)), ad);
				this.ct();
				this.bs();
				this.cs();
				this.clh();
			} else {
				this.ca();
			}
		};
		
		i.bs = function() {
			c.set("_adwb", domainhash, new Date(
					new Date().getTime() + 0.5 * 3600 * 1000));
		};
		
		i.ct = function() {
			c.set("_adwt", timestamp, new Date(
					new Date().getTime() + 24 * 3600 * 1000));
		};
		
		i.b = function() {
			if (c.get("_adwb") == null) {
				this.bs();return false;
			} else {
				this.bs();return true;
			}
		};
		
		i.cs = function() {
			c.set("_adwc", domainhash+ '#' + ec(d.location.href), false);
		};
		
		i.c = function() {
			if (c.get("_adwc") == null) {
				this.cs(); return false;
			} else {
				return true;
			}
		};
		
		i.o = function(on) {
			if (c.get('_adwo') == null) {
				c.set('_adwo', domainhash + "."  + '1' + '.'+ on, ad);
			}else {
				c.set('_adwo', domainhash + "." + (parseInt((c.get('_adwo').split('.'))[1]) + parseInt(1)) + '.'+ on, ad);
			}
		};
		
		i.ef = function(days) {
			var time;
			try{
				if(days == 0){
					time = false;
				}else{
					time = new Date(new Date().getTime() + days * 24 * 3600 * 1000);
				}
			}catch(e){
				time = new Date(new Date().getTime() + 30 * 24 * 3600 * 1000);
			}
			
			c.set("_adwe", domainhash + '#' + ec(d.location.href), time);
		};
		
		i.rf = function(referer) {
			c.set("_adwr", domainhash+ '#' + ec(referer), new Date(new Date().getTime() + 6 * 30 * 24 * 3600 * 1000));
		};

		i.clh = function(){
			c.set("_adwlh", domainhash + '#' + ec(d.location.href), new Date(
					new Date().getTime() + 30 * 3600 * 1000));
		};
	};
	
	var cp = new cp();
	
	var browser = function() {
		
		var i = this;
		i.w = function() {
			return w.screen.width;
		};

		i.h = function() {
			return w.screen.height;
		};

		i.c = function() {
			return w.screen.colorDepth + "-bit";
		};

		i.l = function() {
			var lang = w.navigator.language;
			return lang ? lang : w.navigator.browserLanguage;
		};

		i.j = function() {
			return w.navigator.javaEnabled() ? 1 : 0;
		};

		i.p = function() {
			return d.location.protocol;
		};
		
		i.t = function() {
			return lensplit(d.title,200);
		};
		
		i.lh = function() {
			return this.su(d.location.href);
		};
		
		i.re = function() {
			var refer = d.referrer;
			return refer;
		};
		
		i.kwd = function(){
			var doc = d;
			var keyword = '';
			if (!doc) {
				return "";
			}
			var head=doc.head?doc.head:doc.getElementsByTagName("head").length>0?doc.getElementsByTagName("head")[0]:null;
			if (head==null) {
				return keyword;
			}
			var n = head.firstChild;
			while (n && n != 'undefined') {
				var name = n.nodeName;
				if (name && name.toLowerCase() == 'meta' && (n.httpEquiv && n.httpEquiv.toLowerCase() == 'keywords' || n.name&& n.name.toLowerCase() == 'keywords')) {
					if (n.content && n.content != 'undefined') {
						keyword = keyword + n.content;
					}
				}
				n = n.nextSibling;
			}
			return keyword;
		};
		
		i.dst = function(){
			var doc = d;
			var des='';
			if(!doc){
				return "";
			}
			var head=doc.head?doc.head:doc.getElementsByTagName("head").length>0?doc.getElementsByTagName("head")[0]:null;
			if (head==null) {
				return des;
			}
			var n = head.firstChild;
			while(n){
				var name = n.nodeName;
				if(name && name.toLowerCase()=='meta' && (n.httpEquiv && n.httpEquiv.toLowerCase() == 'description' || n.name && n.name.toLowerCase() == 'description')){
					if(n.content && n.content!='undefined'){
						des = des + n.content;
					}
				}
				n=n.nextSibling;
			}
			return des;
		};
		
		i.su = function (dlh){
           	try{
            		dlh = decodeURIComponent(dlh);
            	}catch(e){
            	}
			var uri = dlh.substring(0, dlh.indexOf("?"));
			if (uri != ""){
				var url = dlh.substring(dlh.indexOf("?") + 1, dlh.length);
				try{
					uri = decodeURIComponent(uri);
				}catch(e){
				}
				var parmeter = url.split("&");
				var urlc ="";
				for ( var i = 0; i < parmeter[l]; i++) {
					var p = parmeter[i].split("=");
					if(p[l] == 1){
						p = parmeter[i];
						urlc = urlc + p + "&";
						continue;
					}
					if(p == ""){
						urlc = urlc + "" + "&";
					} else{
						try{
							val = decodeURIComponent(p[1]);
						}catch(e1){
							val = p[1];
						}
						var pp = p[0] + "=" + val;
						urlc = urlc + pp + "&";
					}
				}
				return uri + "?" + urlc.substring(0,urlc[l]-1);
			} else {
				return decodeURIComponent(dlh);
			}
		};
		
		i.charset = function() {
			return d.characterSet ? d.characterSet : d.charset; 
		};
		
		i.acceptCookie = function() {
			c.set("_adwtc", "t");
			if(c.get("_adwtc") != null){
				c.clear("_adwtc"); 
				return '1';
			} else { 
				return '0';
			}
		};
		
		i.fh = function(){
			var pg = navigator.plugins;
			if (pg && pg[l]) {
				for ( var i = 0; i < pg[l]; i++) {
					if (pg[i].name.indexOf('Shockwave Flash') > -1) {
						return 1;
						break;
					}
				}
				return "0";
			} else if (window.ActiveXObject) {
				var f = 0;
				for ( var j = 9; j >= 6; j--) {
					try {
						var fl = eval("new ActiveXObject('ShockwaveFlash.ShockwaveFlash."
								+ j + "');");
						if (fl) {
							f = 1;
							break;
						}
					} catch (e) {
					}
				}
			    return f;
			 }
		};
	};
	
	var b = new browser;
	
	function getEffectUrl(){
		var cc = c.get("_adwe");
		var effectpageurl = "";
		if (cc != null) {
			effectpageurl = cc.substring(cc.indexOf("#") + 1, cc[l]);
		}
		return decodeURIComponent(effectpageurl);
	}
	
	function getReferer(){
		var rf = c.get("_adwr");
		var refererurl = "";
		if (rf != null) {
			refererurl = rf.substring(rf.indexOf("#") + 1, rf[l]);
		}
		return decodeURIComponent(refererurl);
	}
	
        function referer() {
                var ref = '';
                var lh = b.lh();
                var refer = b.re();
                refer = refer == '' ? "directinto" : refer;
                if (!isNotSelfDomain()) {
                        if (isContainAdw(lh)) {
                                if (!(getReferer() == lh)) {
                                        cp.rf(lh);
                                        ref = lh;
                                }
                        } else {
                                if (!(getReferer() == refer)) {
                                        if (!(refer == "directinto")) {
                                                cp.rf(refer);
                                                ref = refer;
                                        } else if (e) {
                                                cp.rf(refer);
                                                ref = refer;
                                        }
                                }
                        }
                }
                return ec(ref);
        }
	
	function isContainAdw(lh){
		var juge_contain = false;
		Outer: 
		for ( var i = 0; i < ef.length; i++) {
			var ele = ef[i];
			if (typeof (ele) == 'object') {
				for ( var j = 0; j < ele.length; j++) {
					if (lh.indexOf(ele[j]) > 0) {
						juge_contain = true;
						break Outer;
					};
				};
			} else if (typeof (ele) == "string") {
				if (lh.indexOf(ef[i]) > 0) {
					juge_contain = true;
					break Outer;
				};
			};
		}
		return juge_contain;
	}
	
	function isNotSelfDomain(){
		var domain = d.domain;
		var refer = b.re();
		if (window.location.port != "") {
			domain = domain + ":" + window.location.port;
		}
		var referdomain = refer == "" ? "" : refer.split('/')[2];
		return domain == referdomain;
	}
	
	function effect(days) {
		var lh = b.lh();
		var epu = decodeURIComponent(getEffectUrl());
		if (isContainAdw(lh)) {
			if (!isNotSelfDomain()) {
				for ( var i = 0; i < ef.length; i++) {
					var ele = ef[i];
					if (typeof (ele) == 'object') {
						var etlist = new Array();
						var lhlist = new Array();
						for ( var j = 0; j < ele.length; j++) {
							re = new RegExp("^http(?:s)?://.+(?:[?#&]" + ele[j] + "=([^&]+)).*$");
							var lr = lh.match(re);
							var er = epu.match(re);
							var erv = (er == null ? "" : er[1]);
							var lrv = (lr == null ? "" : lr[1]);
							if (erv != "") {
								etlist.push(erv);
							}
							if (lrv != "") {
								lhlist.push(lrv);
							}
						}
						if (lhlist.length > 0) {
							if (etlist.length == 0 || (etlist[0] != lhlist[0])) {
								cp.ef(days);
								return true;
							}
						}
					} else if (typeof (ele) == "string") {
						re = new RegExp("^http(?:s)?://.+(?:[?#&]" + ele + "=([^&]+)).*$");
						var lr = lh.match(re);
						var er = epu.match(re);
						if ((lr == null ? "" : lr[1]) != (er == null ? "" : er[1])) {
							cp.ef(days);
							return true;
						}
					}
				}
				return false;
			}
		}
	}
	
	var createImg = function(url) {
		var img = new Image(1, 1); 
		img.onload=function(){
            img.onload=null;
        };
        img.src = url;
    };
    
    var effectRD = 30;
    var _setEffectRD = function(days) {
    	if(!isNaN(days)){
    		effectRD = days;
    	}
    };
    
	var ourl, aurl, curl;
	
    var _setAction = function(actID, attr) {
    	var ac = c.get("_adwp");
		var cc = c.get("_adwe");
		var effectpageurl;
		if (cc == null) {
			effectpageurl = "";
		} else {
			effectpageurl = cc.substring(cc.indexOf("#") + 1, cc[l]);
		}
		 
     		var lc = c.get('_adwlh');
		var lastpageurl;
		if(lc == null){
			lastpageurl = '';
		}else{
			lastpageurl = lc.substring(lc.indexOf('#') + 1, lc[l]);
		}

		if (ac != null) {
			var acq = ac.split(".");
			uid = acq[2] + acq[1];
			sid = uid + acq[5];
			if(!attr){
				attr = '';
			} else {
				attr = lensplit(attr,150);
			}
			
			aurl = domainurl(account) + '/_adwa.gif' + '?adwu=' + uid + '&adws=' + sid + '&adwactid=' + actID + '&attr=' + ec(attr) + '&adweu=' + ec(b.su(decodeURIComponent(effectpageurl))) + '&adwmc=' + mc() + '&adwa=' + account + '&encoding=' + b.charset() +  '&adwlh=' + ec(b.lh()) + '&cmp=' + ((lastpageurl == effectpageurl) ? "1" : "0");
			new createImg(aurl);
			aurl = aurl.replace("_adwa.gif", "_adwa2.gif");
			new createImg(aurl);
		}
	};

	var _tmpJudge = '';

	var gon;
	var _dataType = 'order', _customer = '', _rid = '', _page_groups_id = '', _page_url = '';
	var _setOrder = function(on, op, attr) {
		gon = on;
		if(!attr){
			attr = '';
		}else {
			attr = lensplit(attr,150);
		}
		ourl = '&on=' + ec(on) + '&op=' + op + '&attr=' + ec(attr);
	};

	var items = new Array();
	
	var _setItem = function(pn, pna, pp, ta, ct, ctn) {
		items.push([pn, pna, pp, ta, ct, ctn]); 
	};
	
	var _setDataType = function(dataType) {
		_dataType = dataType;
	};

	var _setCustomer = function(customer){
		_customer = customer;	
	};
	
	var _setRuleid = function(rid) {
		_rid = rid;
	};

	var _setTmpJudge = function(tj) {
		_tmpJudge = tj;
	};

	var _setPageGroup = function(pg) {
		_page_groups_id = _page_groups_id + pg + ",";
	};

	var _setPageUrl = function(pu) {
		_page_url = pu;
		_trackPageview();
	};

	var _trackTrans = function() {
		var i = this;
		i.sub = function(subobj) {
			return subobj.substring(0, subobj[l] - 1);
		};
		var pn='',pna='',pp='',ta='',ct='',ctn='';
		for (var j =0; j < items[l]; j++) {
			pn += items[j][0]; pn += '|';
			pna += items[j][1]; pna += '|';
			pp += items[j][2]; pp += '|';
			ta += items[j][3]; ta += '|';
			ct += items[j][4]; ct += '|';
			ctn += items[j][5]; ctn += '|';
		}
		dcurl = ourl;
		ourl += '&pn='+ec(sub(pn))+'&pp='+ec(sub(pp))+'&ta='+ec(sub(ta))+'&ct='+ec(sub(ct))+'&ctn='+ec(sub(ctn)) + '&adwa=' + account + '&encoding=' + b.charset() + '&datatype=' + _dataType + '&customer=' + _customer;
		var ac = c.get('_adwp');
		var cc = c.get('_adwe');
		var effectpageurl;
		if(cc == null){
			effectpageurl = '';
		} else {
			effectpageurl = cc.substring(cc.indexOf('#') + 1, cc[l]);
		}

		var lc = c.get('_adwlh');
		var lastpageurl;
		if(lc == null){
			lastpageurl = '';
		}else{
			lastpageurl = lc.substring(lc.indexOf('#') + 1, lc[l]);
		}
		

		var oc = c.get('_adwo');
		
		if (ac != null) {
			var acq = ac.split(".");
			uid = acq[2] + acq[1];
			sid = uid + acq[5];
			ourl =  domainurl(account) + '/_adwo.gif' + '?adwu=' + uid + '&adws=' + sid + '&adweu=' + ec(b.su(decodeURIComponent(effectpageurl))) + ourl + '&cmp=' + ((lastpageurl == effectpageurl) ? "1" : "0");

			pnau = '&pna='+ec(sub(pna));

                        if (navigator.userAgent.indexOf("MSIE 6.0") > 0 || navigator.userAgent.indexOf("MSIE 7.0") > 0) {
                                if ((ourl + pnau).length < 2000) {
                                        ourl = ourl + pnau;
                                }else{
                                        ourl = ourl + "&pna=";
                                }
                        } else {
                                if ((ourl + pnau).length < 6000) {
                                        ourl = ourl + pnau;
                                }else{
                                        ourl = ourl + "&pna=";
                                }
                        }


			if(gon != undefined && gon != ''){
				if(oc != null) {
					if((oc.split('.')[2]) === gon)
					return;
				}
				cp.o(gon);
			}

			new createImg(ourl.replace("_adwo.gif", "_adwo2.gif") + '&mc=' + mc());
			if(_dataType=="order"){
			    new createImg(ourl);
			}
		}
		gon='';
		ourl='';
		items = new Array();
	};
	
	var Log = function() {
		var i = this;
		var url; 
		i.acquireCookie = function() {
			if (jg) {
				var ct = c.get("_adwt");
				var cc = new Date();
				var o = new Date(ct*1000);
				if(!(o.getDate() == cc.getDate())){
					cp.ua();
				}
			}
			
			var ac = c.get("_adwp");
			if (ac != null) {
				var cc = c.get("_adwe");
				var effectpageurl;
				if (cc == null) {
					effectpageurl = "";
				} else {
					effectpageurl = cc.substring(cc.indexOf("#") + 1, cc[l]);
				}

				var lastpageurl;
				var lc = c.get('_adwlh');
				if(lc == null){
					lastpageurl = '';
				}else{
					lastpageurl = lc.substring(lc.indexOf('#') + 1, lc[l]);
				}
				
				var acq = ac.split(".");
				uid = acq[2] + acq[1];
				sid = uid + acq[5];
				url = '?adwu=' + uid + '&adws=' + sid + '&adwft=' + acq[2] + '&adwpt=' + acq[3] + '&adwv=' + acq[5] + '&adweu=' + ec(b.su(decodeURIComponent(effectpageurl)))+'&cmp=' + ((lastpageurl == effectpageurl) ? "1" : "0");
			} else {
				url = '?adwu=' + ncu + '&adws=' + ncu + Math.round(Math.random() * 1000000000000000000);
			}
		};
		
		i.acquireBrowser = function() {
			__pageurl = _page_url == "" ? ec(b.lh()) : ec(_page_url);

			url += '&adwsw=' + b.w() + '&adwsh=' + b.h() + '&adwmc=' + mc() + '&adwlh=' + __pageurl + '&adwr=' + ec(b.re())
					+ '&adwt=' + ec(b.t()) + '&adwsc=' + b.c()
					+ '&adwl=' + b.l() + '&adwj=' + b.j() + '&adwp=' + ec(b.p())
					+ '&adwfv=' + b.fh() + '&adwac=' + b.acceptCookie() + '&adwa=' + account + '&adwe=' + e + '&adwcr=' + referer()
					+ '&encoding=' + b.charset() + '&drid=' + _rid  + '&pgi=' + _page_groups_id.substring(0, _page_groups_id.length-1);
			e = false;
		};
		
        i.sendlog = function() {
			this.acquireCookie();
			this.acquireBrowser();
			specialurl = '&kwd=' + b.kwd() + '&dst=' + b.dst();
			if (navigator.userAgent.indexOf("MSIE 6.0") > 0 || navigator.userAgent.indexOf("MSIE 7.0") > 0) {
				for ( var i = 0; i < specialurl.length; i++) {
					if (url.length < 2000) {
						if(specialurl.charAt(i)=="&" || specialurl.charAt(i) == "="){
							url = url + specialurl.charAt(i);
							continue;
						}
						url = url + ec(specialurl.charAt(i));
					} else {
						break;
					}
				}
			}else{
				for ( var i = 0; i < specialurl.length; i++) {
					if (url.length < 6000) {
						if(specialurl.charAt(i)=="&" || specialurl.charAt(i) == "="){
							url = url + specialurl.charAt(i);
							continue;
						}
						url = url + ec(specialurl.charAt(i));
					} else {
						break;
					}
				}
 			}
			var ebtrack = function() {
				url = domainurl(account)+ '/_adw.gif' + url;
				new createImg(url);
			}
			/*var adwcm = function() {
				if(account!='hcdwb'){
					if(account !='dj5p1'){
						adwcmurl = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'cm.emarbox.com/_cm?pt=3';
						new createImg(adwcmurl);
					}
				}
			};*/
			setTimeout(ebtrack, 1);
			//setTimeout(adwcm, 1001);
		};
	};
	
	var tracker = function(){
		var i = this;
		i._initData = function(){
			var effect_flag = effect(effectRD);
			var iab = cp.b(); 
			var iac = cp.c();
			if(!cp.ca()) {
				if(!iab || !iac){
					cp.ua();
				} else {
					cp.ca();
					if(effect_flag){
						cp.ua();
					}
				};
			};
			var L = new Log;
			L.sendlog(); 
		};
	};
	
	var _setDomainName = function(Domain){
		CDomain = Domain;
	};
	
	var a = new tracker;
	var _setAccount = function(a) {
		account = a;
		var f = arguments;
	};
	
	var _trackPageview = function() {
		var t = new tracker;
		t._initData();
	};
	
	var Fa = function() {
		var i = this;
		i.push = function() {
			var args = arguments, m = 0;
			for ( var j = 0; j < args[l]; j++) {
				try {
					if (typeof args[j] === "function")
						args[j]();
					else {
						var o = args[j][0];
						eval(o).apply(window,args[j].slice(1));
					}
				} catch (d) {
				        var errurl = ('https:' == location['protocol'] ? 'https:':'http') + '://err.emarbox.com';
					new createImg(errurl+"/_adwerr.gif?adwa="+account+"&url="+ec(b.lh())+"&referer="+ec(b.re()));
				}
			}
			return m;
		};
	};
	
	var adwq = window[wa];

	var Ea = new Fa;

	if (adwq && typeof adwq.push == "function") {
		if (adwq.constructor === Array) {
			window[wa] = Ea;
			for ( var j = 0; j < adwq[l]; ++j) {
				Ea.push(adwq[j]); 
			}
		}
	}
})();;
