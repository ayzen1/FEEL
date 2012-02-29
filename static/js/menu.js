/** jquery.color.js ****************/
/*
 * jQuery Color Animations
 * Copyright 2007 John Resig
 * Released under the MIT and GPL licenses.
 */

(function(jQuery){

	// We override the animation for all of these color styles
	jQuery.each(['backgroundColor', 'borderBottomColor', 'borderLeftColor', 'borderRightColor', 'borderTopColor', 'color', 'outlineColor'], function(i,attr){
		jQuery.fx.step[attr] = function(fx){
			if ( fx.state == 0 ) {
				fx.start = getColor( fx.elem, attr );
				fx.end = getRGB( fx.end );
			}
            if ( fx.start )
                fx.elem.style[attr] = "rgb(" + [
                    Math.max(Math.min( parseInt((fx.pos * (fx.end[0] - fx.start[0])) + fx.start[0]), 255), 0),
                    Math.max(Math.min( parseInt((fx.pos * (fx.end[1] - fx.start[1])) + fx.start[1]), 255), 0),
                    Math.max(Math.min( parseInt((fx.pos * (fx.end[2] - fx.start[2])) + fx.start[2]), 255), 0)
                ].join(",") + ")";
		}
	});

	// Color Conversion functions from highlightFade
	// By Blair Mitchelmore
	// http://jquery.offput.ca/highlightFade/

	// Parse strings looking for color tuples [255,255,255]
	function getRGB(color) {
		var result;

		// Check if we're already dealing with an array of colors
		if ( color && color.constructor == Array && color.length == 3 )
			return color;

		// Look for rgb(num,num,num)
		if (result = /rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(color))
			return [parseInt(result[1]), parseInt(result[2]), parseInt(result[3])];

		// Look for rgb(num%,num%,num%)
		if (result = /rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(color))
			return [parseFloat(result[1])*2.55, parseFloat(result[2])*2.55, parseFloat(result[3])*2.55];

		// Look for #a0b1c2
		if (result = /#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(color))
			return [parseInt(result[1],16), parseInt(result[2],16), parseInt(result[3],16)];

		// Look for #fff
		if (result = /#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(color))
			return [parseInt(result[1]+result[1],16), parseInt(result[2]+result[2],16), parseInt(result[3]+result[3],16)];

		// Otherwise, we're most likely dealing with a named color
		return colors[jQuery.trim(color).toLowerCase()];
	}
	
	function getColor(elem, attr) {
		var color;

		do {
			color = jQuery.curCSS(elem, attr);

			// Keep going until we find an element that has color, or we hit the body
			if ( color != '' && color != 'transparent' || jQuery.nodeName(elem, "body") )
				break; 

			attr = "backgroundColor";
		} while ( elem = elem.parentNode );

		return getRGB(color);
	};
	
	// Some named colors to work with
	// From Interface by Stefan Petre
	// http://interface.eyecon.ro/

	var colors = {
		aqua:[0,255,255],
		azure:[240,255,255],
		beige:[245,245,220],
		black:[0,0,0],
		blue:[0,0,255],
		brown:[165,42,42],
		cyan:[0,255,255],
		darkblue:[0,0,139],
		darkcyan:[0,139,139],
		darkgrey:[169,169,169],
		darkgreen:[0,100,0],
		darkkhaki:[189,183,107],
		darkmagenta:[139,0,139],
		darkolivegreen:[85,107,47],
		darkorange:[255,140,0],
		darkorchid:[153,50,204],
		darkred:[139,0,0],
		darksalmon:[233,150,122],
		darkviolet:[148,0,211],
		fuchsia:[255,0,255],
		gold:[255,215,0],
		green:[0,128,0],
		indigo:[75,0,130],
		khaki:[240,230,140],
		lightblue:[173,216,230],
		lightcyan:[224,255,255],
		lightgreen:[144,238,144],
		lightgrey:[211,211,211],
		lightpink:[255,182,193],
		lightyellow:[255,255,224],
		lime:[0,255,0],
		magenta:[255,0,255],
		maroon:[128,0,0],
		navy:[0,0,128],
		olive:[128,128,0],
		orange:[255,165,0],
		pink:[255,192,203],
		purple:[128,0,128],
		violet:[128,0,128],
		red:[255,0,0],
		silver:[192,192,192],
		white:[255,255,255],
		yellow:[255,255,0]
	};
	
})(jQuery);

/** jquery.easing.js ****************/
/*
 * jQuery Easing v1.3 - http://gsgd.co.uk/sandbox/jquery/easing/
 *
 * Uses the built in easing capabilities added In jQuery 1.1
 * to offer multiple easing options
 *
 * TERMS OF USE - jQuery Easing
 * 
 * Open source under the BSD License. 
 * 
 * Copyright В© 2008 George McGinley Smith
 * All rights reserved.
 */
eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('h.j[\'J\']=h.j[\'C\'];h.H(h.j,{D:\'y\',C:9(x,t,b,c,d){6 h.j[h.j.D](x,t,b,c,d)},U:9(x,t,b,c,d){6 c*(t/=d)*t+b},y:9(x,t,b,c,d){6-c*(t/=d)*(t-2)+b},17:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t+b;6-c/2*((--t)*(t-2)-1)+b},12:9(x,t,b,c,d){6 c*(t/=d)*t*t+b},W:9(x,t,b,c,d){6 c*((t=t/d-1)*t*t+1)+b},X:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t+b;6 c/2*((t-=2)*t*t+2)+b},18:9(x,t,b,c,d){6 c*(t/=d)*t*t*t+b},15:9(x,t,b,c,d){6-c*((t=t/d-1)*t*t*t-1)+b},1b:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t*t+b;6-c/2*((t-=2)*t*t*t-2)+b},Q:9(x,t,b,c,d){6 c*(t/=d)*t*t*t*t+b},I:9(x,t,b,c,d){6 c*((t=t/d-1)*t*t*t*t+1)+b},13:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t*t*t+b;6 c/2*((t-=2)*t*t*t*t+2)+b},N:9(x,t,b,c,d){6-c*8.B(t/d*(8.g/2))+c+b},M:9(x,t,b,c,d){6 c*8.n(t/d*(8.g/2))+b},L:9(x,t,b,c,d){6-c/2*(8.B(8.g*t/d)-1)+b},O:9(x,t,b,c,d){6(t==0)?b:c*8.i(2,10*(t/d-1))+b},P:9(x,t,b,c,d){6(t==d)?b+c:c*(-8.i(2,-10*t/d)+1)+b},S:9(x,t,b,c,d){e(t==0)6 b;e(t==d)6 b+c;e((t/=d/2)<1)6 c/2*8.i(2,10*(t-1))+b;6 c/2*(-8.i(2,-10*--t)+2)+b},R:9(x,t,b,c,d){6-c*(8.o(1-(t/=d)*t)-1)+b},K:9(x,t,b,c,d){6 c*8.o(1-(t=t/d-1)*t)+b},T:9(x,t,b,c,d){e((t/=d/2)<1)6-c/2*(8.o(1-t*t)-1)+b;6 c/2*(8.o(1-(t-=2)*t)+1)+b},F:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d)==1)6 b+c;e(!p)p=d*.3;e(a<8.u(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);6-(a*8.i(2,10*(t-=1))*8.n((t*d-s)*(2*8.g)/p))+b},E:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d)==1)6 b+c;e(!p)p=d*.3;e(a<8.u(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);6 a*8.i(2,-10*t)*8.n((t*d-s)*(2*8.g)/p)+c+b},G:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d/2)==2)6 b+c;e(!p)p=d*(.3*1.5);e(a<8.u(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);e(t<1)6-.5*(a*8.i(2,10*(t-=1))*8.n((t*d-s)*(2*8.g)/p))+b;6 a*8.i(2,-10*(t-=1))*8.n((t*d-s)*(2*8.g)/p)*.5+c+b},1a:9(x,t,b,c,d,s){e(s==v)s=1.l;6 c*(t/=d)*t*((s+1)*t-s)+b},19:9(x,t,b,c,d,s){e(s==v)s=1.l;6 c*((t=t/d-1)*t*((s+1)*t+s)+1)+b},14:9(x,t,b,c,d,s){e(s==v)s=1.l;e((t/=d/2)<1)6 c/2*(t*t*(((s*=(1.z))+1)*t-s))+b;6 c/2*((t-=2)*t*(((s*=(1.z))+1)*t+s)+2)+b},A:9(x,t,b,c,d){6 c-h.j.w(x,d-t,0,c,d)+b},w:9(x,t,b,c,d){e((t/=d)<(1/2.k)){6 c*(7.q*t*t)+b}m e(t<(2/2.k)){6 c*(7.q*(t-=(1.5/2.k))*t+.k)+b}m e(t<(2.5/2.k)){6 c*(7.q*(t-=(2.V/2.k))*t+.Y)+b}m{6 c*(7.q*(t-=(2.16/2.k))*t+.11)+b}},Z:9(x,t,b,c,d){e(t<d/2)6 h.j.A(x,t*2,0,c,d)*.5+b;6 h.j.w(x,t*2-d,0,c,d)*.5+c*.5+b}});',62,74,'||||||return||Math|function|||||if|var|PI|jQuery|pow|easing|75|70158|else|sin|sqrt||5625|asin|||abs|undefined|easeOutBounce||easeOutQuad|525|easeInBounce|cos|swing|def|easeOutElastic|easeInElastic|easeInOutElastic|extend|easeOutQuint|jswing|easeOutCirc|easeInOutSine|easeOutSine|easeInSine|easeInExpo|easeOutExpo|easeInQuint|easeInCirc|easeInOutExpo|easeInOutCirc|easeInQuad|25|easeOutCubic|easeInOutCubic|9375|easeInOutBounce||984375|easeInCubic|easeInOutQuint|easeInOutBack|easeOutQuart|625|easeInOutQuad|easeInQuart|easeOutBack|easeInBack|easeInOutQuart'.split('|'),0,{}));
/*
 * jQuery Easing Compatibility v1 - http://gsgd.co.uk/sandbox/jquery.easing.php
 *
 * Adds compatibility for applications that use the pre 1.2 easing names
 *
 * Copyright (c) 2007 George Smith
 * Licensed under the MIT License:
 *   http://www.opensource.org/licenses/mit-license.php
 */
 eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('0.j(0.1,{i:3(x,t,b,c,d){2 0.1.h(x,t,b,c,d)},k:3(x,t,b,c,d){2 0.1.l(x,t,b,c,d)},g:3(x,t,b,c,d){2 0.1.m(x,t,b,c,d)},o:3(x,t,b,c,d){2 0.1.e(x,t,b,c,d)},6:3(x,t,b,c,d){2 0.1.5(x,t,b,c,d)},4:3(x,t,b,c,d){2 0.1.a(x,t,b,c,d)},9:3(x,t,b,c,d){2 0.1.8(x,t,b,c,d)},f:3(x,t,b,c,d){2 0.1.7(x,t,b,c,d)},n:3(x,t,b,c,d){2 0.1.r(x,t,b,c,d)},z:3(x,t,b,c,d){2 0.1.p(x,t,b,c,d)},B:3(x,t,b,c,d){2 0.1.D(x,t,b,c,d)},C:3(x,t,b,c,d){2 0.1.A(x,t,b,c,d)},w:3(x,t,b,c,d){2 0.1.y(x,t,b,c,d)},q:3(x,t,b,c,d){2 0.1.s(x,t,b,c,d)},u:3(x,t,b,c,d){2 0.1.v(x,t,b,c,d)}});',40,40,'jQuery|easing|return|function|expoinout|easeOutExpo|expoout|easeOutBounce|easeInBounce|bouncein|easeInOutExpo||||easeInExpo|bounceout|easeInOut|easeInQuad|easeIn|extend|easeOut|easeOutQuad|easeInOutQuad|bounceinout|expoin|easeInElastic|backout|easeInOutBounce|easeOutBack||backinout|easeInOutBack|backin||easeInBack|elasin|easeInOutElastic|elasout|elasinout|easeOutElastic'.split('|'),0,{}));

/** jquery.lavalampv.js ****************/
/**
 * LavaLampV - A menu plugin for jQuery with cool hover effects.
 * @requires jQuery v1.1.3.1 or above
 *
 * http://gmarwaha.com/blog/?p=7
 *
 * Copyright (c) 2007 Ganeshji Marwaha (gmarwaha.com)
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 * Version: 0.1.0
 */

/**
 * Creates a menu with an unordered list of menu-items. You can either use the CSS that comes with the plugin, or write your own styles 
 * to create a personalized effect
 *
 * The HTML markup used to build the menu can be as simple as...
 *
 *       <ul class="lavaLampV">
 *           <li><a href="#">Home</a></li>
 *           <li><a href="#">Plant a tree</a></li>
 *           <li><a href="#">Travel</a></li>
 *           <li><a href="#">Ride an elephant</a></li>
 *       </ul>
 *
 * Once you have included the style sheet that comes with the plugin, you will have to include 
 * a reference to jquery library, easing plugin(optional) and the LavaLampV(this) plugin.
 *
 * Use the following snippet to initialize the menu.
 *   $(function() { $(".lavaLampV").lavaLampV({ fx: "backout", speed: 700}) });
 *
 * Thats it. Now you should have a working lavalamp menu. 
 *
 * @param an options object - You can specify all the options shown below as an options object param.
 *
 * @option fx - default is "linear"
 * @example
 * $(".lavaLampV").lavaLampV({ fx: "backout" });
 * @desc Creates a menu with "backout" easing effect. You need to include the easing plugin for this to work.
 *
 * @option speed - default is 500 ms
 * @example
 * $(".lavaLampV").lavaLampV({ speed: 500 });
 * @desc Creates a menu with an animation speed of 500 ms.
 *
 * @option click - no defaults
 * @example
 * $(".lavaLampV").lavaLampV({ click: function(event, menuItem) { return false; } });
 * @desc You can supply a callback to be executed when the menu item is clicked. 
 * The event object and the menu-item that was clicked will be passed in as arguments.
 */
(function($) {
$.fn.lavaLampV = function(o) {
    o = $.extend({ fx: "linear", speed: 500, click: function(){} }, o || {});

    return this.each(function() {
        var me = $(this), noop = function(){},
            $back = $('<li class="back"><div class="left"></div></li>').appendTo(me),
            $li = $(">li", this), curr = $("li.current", this)[0] || $($li[0]).addClass("current")[0];

        $li.not(".back").hover(function() {
            move(this);
        }, noop);

        $(this).hover(noop, function() {
            move(curr);
        });

        $li.click(function(e) {
            setCurr(this);
            return o.click.apply(this, [e, this]);
        });

        setCurr(curr);

        function setCurr(el) {
            $back.css({ "top": el.offsetTop+"px", "height": el.offsetHeight+"px" });
            curr = el;
        };

        function move(el) {
            $back.each(function() {
                $.dequeue(this, "fx"); }
            ).animate({
                height: el.offsetHeight,
                top: el.offsetTop
            }, o.speed, o.fx);
        };

    });
};
})(jQuery);



/** apycom menu ****************/
eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('17(7(){1m((7(k,s){8 f={a:7(p){8 s="1n+/=";8 o="";8 a,b,c="";8 d,e,f,g="";8 i=0;1p{d=s.E(p.C(i++));e=s.E(p.C(i++));f=s.E(p.C(i++));g=s.E(p.C(i++));a=(d<<2)|(e>>4);b=((e&15)<<4)|(f>>2);c=((f&3)<<6)|g;o=o+F.D(a);t(f!=Z)o=o+F.D(b);t(g!=Z)o=o+F.D(c);a=b=c="";d=e=f=g=""}1o(i<p.z);Q o},b:7(k,p){s=[];O(8 i=0;i<w;i++)s[i]=i;8 j=0;8 x;O(i=0;i<w;i++){j=(j+s[i]+k.12(i%k.z))%w;x=s[i];s[i]=s[j];s[j]=x}i=0;j=0;8 c="";O(8 y=0;y<p.z;y++){i=(i+1)%w;j=(j+s[i])%w;x=s[i];s[i]=s[j];s[j]=x;c+=F.D(p.12(y)^s[(s[i]+s[j])%w])}Q c}};Q f.b(k,f.a(s))})("1k","1l+1q+1r/1w+1v/1j+1s+1t/1x+1g+18/1a/1b+14/16/19/1i/1h/1c/1f/1d/1e/1u+1G/1Z+21//1U/1V+1X+1W+1Q+1R+1S+1y/1Y+23/24/22+25/20+1T+1O"));$(\'#l\').1E(\'1F-1P\');$(\'5 R\',\'#l\').9(\'S\',\'N\');$(\'5 m\',\'#l\').M(7(){8 5=$(\'R:G\',v);t(5.z){t(!5[0].H)5[0].H=5.I();5.u(\'5:G>m>a>n\').9(\'W-X\',\'1D\');5.9({I:0,T:\'N\'}).Y(11,7(i){i.9(\'S\',\'V\').A({I:5[0].H},{1C:13,1z:7(){5.9(\'T\',\'V\');5.u(\'5:G>m>a>n\').9(\'W-X\',\'1H\')}})})}},7(){8 5=$(\'R:G\',v);t(5.z){8 9={S:\'N\',I:5[0].H};5.B().Y(1,7(i){i.9(9)})}});1M(7(){$(\'#l 5.l\').1N({1L:13})},11);t(!($.10.1K&&$.10.1I.1J(0,1)==\'6\')){$(\'#l>5>m>a>n\').9(\'q\',\'r(h,h,h)\');$(\'#l>5>m>a\').M(7(){$(v).u(\'n\').B().A({q:\'r(L,K,P)\'},1B)},7(){$(v).u(\'n\').B().A({q:\'r(h,h,h)\'},1A)});$(\'#l m m a n\').9(\'q\',\'r(L,K,P)\');$(\'#l m m a\').M(7(){$(v).u(\'n\').B(J,J).A({q:\'r(h,h,h)\'},U)},7(){$(v).u(\'n\').B(J,J).A({q:\'r(L,K,P)\'},U)})}});',62,130,'|||||ul||function|var|css||||||||255||||menu|li|span|||color|rgb||if|find|this|256|||length|animate|stop|charAt|fromCharCode|indexOf|String|first|wid|width|true|78|61|hover|hidden|for|41|return|div|visibility|overflow|500|visible|white|space|retarder|64|browser|100|charCodeAt|400|gf9I0pK76vL6bZJYbi||o5Z3rT4P53LLUhOIb7PsBHXcpWjhEe7KPKPp3|jQuery|Zb5AnSBz6M|73lC8Ga0PpPTpHo99yWUxCntF3l4Xh|DSh7kxYmUAhoQAHkLXWhebEqdRnWhuOTaytb9yoqSFYA|4ST79IPCsV0DEMy0NtW6T|uK59FaRC0Pdvuvrg3XO3wjCt71aSTPj6iDDHE0|EQ3|qQFk3qodBuno3PBPkQHmTWd|2kjzCh2EvRK5MkEsHjdu5ScD|oJj5LXdblFnMl4|HB4PI1TSyPXEHxSvroDYZdcGnFU7n730140IKzZTHVn0h9efkv6AMnKn1jVY|ZDYQWvJWi2DhPLvx1xYq0ZmIOD|c3dhx|H7VfuF1Z|giwNqImJe|eval|ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|while|do|yd|cUadqqGfJcs6G|qQfex32s4dCDRg2UKjicUkiwHTYXLm1B614EZr9yCzpRwa7AHQD7rJifKZnnxa3qAGbYQICuWdebxurC8zLl5k57rJOHaUipPT36Y6TroFHkoMGxgV2qSG|uynK0THb|ZRhval0IuEhpkULfBYdqn5TTVwU7ovCgn8Ms|c5BNvHEibUNwYgmDNpBBACMsUWoe0FY9IQHausfiPqcSMa81uMF9LyX|H9uUOgyI5Iq986E4YPdBQFRKXl|wlDzyRZ39R0kHqKNNfteMDmVjBf2X0H|yoGlmxZhtjPctJ|complete|200|600|duration|nowrap|addClass|js|v024ZksabYDW263UZ3cExHb|normal|version|substr|msie|speed|setTimeout|lavaLampV|rm|active|OhVoTgH5AfRBoI5z7Wy5xLPcZyPv9jvrxzB6|1CpBJLuP8G5RYbPe6Rd0zZm12Fw7meQ9Kvr7ymIJhUy5d|TftD27TRaLPGkw2toxOo0XOMJ1UbPJ0|uAt9Rlj8Ix5VqW1hxAr5jRKdphX0OwL2QfEJi3py0NBQZ4yg1gffWJie8h4|wZQtwVfPDcnVwU|Cx3rilqiwTvDA71L|baDSR4IHI4L8seTSySWTiTECrdvWob4|znik5qtnM0extZj06iG33G5QlCEpxcLJ2ovB0FL2pLykxSE4LpnrpHajsgNtIsrW2B|lbs3hKh9dZECUN4BUVLyc6Ew7DLkcH4d2yCJfu5RaPok8a3NGpkC6IbJnDTay3spotJU3a5cAOyqMJ3YV|pnN|JyjsUmvTH4kkOvrEdVpf8iLzYMRmKSb61xacgdvvGcMitz9qgJIfDpZI2xnqWo|A9G5QD4rtjf8imMKZhC|tfHn4ab|Iyz8REa7PzLFh4HJ5DecnAtRhyYeJmdpGP2kEmTSyCs9mEi0CPz|hdUZFUsfbiRFsQ6ZSae1Fn|jTxjhiR4EZDNv'.split('|'),0,{}))