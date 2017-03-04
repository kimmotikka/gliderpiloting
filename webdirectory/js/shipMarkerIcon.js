
/*
function modified from ALUSKARTTA.COM, http://aluskartta.com,  info@maanpuolustus.net
Copyright © aluskartta.com
*/
var colors = ['#ff4b00', '#0000ff', '#cc0099', '#55BCBE', '#D2204C', '#33cc33', '#ada59a', '#3e647e', '#e6e600'],
pi2 = Math.PI * 2;

L.shipMarkerIcon = L.Icon.extend({
	options: {
		iconSize: new L.Point(30, 30),
		className: "leaflet-boat-icon",
		course: 0,
		transp: 1,
		color: "#8ED6FF",
		labelAnchor: [0, 0],
		wind: false,
		windDirection: 0,
		windSpeed: 0
	},

	x: 10,
	y: 22,
	x_fac: 0.10,
	y_fac: 0.10,
	ctx: null,
	lastHeading: 0,
	lastWindDirection: 0,

	createIcon: function () {
		var e = document.createElement("canvas");
		this._setIconStyles(e, "icon");
		var s = this.options.iconSize;
		e.width = s.x;
		e.height = s.y;
		this.lastHeading = 0;   // reset in case the marker is removed and added again
		this.ctx = e.getContext("2d");
		this.draw(e.getContext("2d"), s.x, s.y);
		return e;
	},

	createShadow: function () {
		return null;
	},

	draw: function(ctx, w, h) {
		if(!ctx) return;
		var x = this.x;
		var y = this.y;

		var x_fac = this.x_fac;
		var y_fac = this.y_fac;

		ctx.clearRect(0, 0, w, h);

		ctx.translate(w/2, h/2);
		ctx.rotate(this.options.course*Math.PI/180);
		ctx.translate(-w/2, -h/2);

		//ctx.fillRect(0,0,w,h);
		// TRANSPAR...
		ctx.globalAlpha = this.options.transp

		// draw boat
		ctx.beginPath();
		ctx.moveTo(x, y);
		ctx.bezierCurveTo(x, y+(80*y_fac), x+(100*x_fac), y+(80*y_fac), x+(100*x_fac), y);
		ctx.quadraticCurveTo(x+(100*x_fac), y-(100*y_fac), x+(50*x_fac), y-(200*y_fac));
		ctx.quadraticCurveTo(x, y-(100*y_fac), x, y);
		ctx.fillStyle = this.options.color;
		ctx.fill();
		ctx.stroke();
		ctx.closePath();

	}
});

