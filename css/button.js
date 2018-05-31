function lol() {
	if (lel == "1") {
		document.documentElement.style.setProperty("--Back", "#181a1d");
		document.documentElement.style.setProperty("--Div", "#1c1e21");
		document.documentElement.style.setProperty("--DivHover", "#26292e");
		document.documentElement.style.setProperty("--ColorH4", "#dcdddf");
		document.documentElement.style.setProperty("--ColorP", "grey");
		document.documentElement.style.setProperty("--ColorBut", "#292c30");
		document.cookie = "lel=1";
		lel = "2"
	} else if (lel == "2"){
		document.documentElement.style.setProperty("--Back", "white");
		document.documentElement.style.setProperty("--Div", "white");
		document.documentElement.style.setProperty("--DivHover", "white");
		document.documentElement.style.setProperty("--ColorH4", "black");
		document.documentElement.style.setProperty("--ColorP", "grey");
		document.documentElement.style.setProperty("--ColorBut", "#e2e5e9");
		document.cookie = "lel=2";
		lel = "1"} }
document.documentElement.style.setProperty("--HeightBut", "25px");
document.documentElement.style.setProperty("--HeightButMob", "50px");
if (document.cookie == ""){	var lel = "1"
} else { lel = document.cookie.replace("lel=", "")}
lol();