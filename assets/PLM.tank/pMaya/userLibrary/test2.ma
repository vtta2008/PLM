//Maya ASCII 2017ff04 scene
//Name: test2.ma
//Last modified: Sat, May 13, 2017 06:22:40 AM
//Codeset: 1252
requires maya "2017ff04";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201702071345-1015190";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "Style_Arrow_3D";
	rename -uid "22CD670E-4137-FFB5-5AF3-7490E0451D1B";
createNode nurbsCurve -n "Style_Arrow_3DShape" -p "Style_Arrow_3D";
	rename -uid "13B98D5A-467C-AC61-D415-02B6054A09D5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-2.0857863095420344 -9.3632573363181929e-025 5.0971193932269898e-009
		2.0857863095420335 2.8284273758870384 -1.0846335936285916e-016
		1.590596160198142 2.221060656850975 -8.5172312446305679e-017
		1.2229632672818953 1.5289659825354958 -5.863215305831422e-017
		0.99353414115743632 0.77962543257589201 -2.989675258513013e-017
		0.91421332817924306 -7.8384805911619546e-025 4.2670694477831006e-009
		-2.0857863095420344 -9.3632573363181929e-025 5.0971193932269898e-009
		2.0857863095420339 -5.1957367987512135e-016 2.8284273758870384
		1.5905961601981407 -4.0800222655138452e-016 2.2210606728157671
		1.2229632672818962 -2.8086649577231904e-016 1.5289659895836587
		0.99353414115743455 -1.4321487083376504e-016 0.779625444841058
		0.91421332817924306 -7.8384805911619546e-025 4.2670694477831006e-009
		0.99353414115743632 1.4321486858069046e-016 -0.77962543257589201
		1.2229632672818953 2.8086649447759225e-016 -1.5289659825354958
		1.590596160198142 4.0800222361869959e-016 -2.221060656850975
		2.0857863095420335 5.1957367987512135e-016 -2.8284273758870384
		-2.0857863095420344 -9.3632573363181929e-025 5.0971193932269898e-009
		;
createNode partition -n "mtorPartition";
	rename -uid "D582B191-4754-66ED-FF53-0DA05D95C2CD";
	addAttr -s false -ci true -sn "rgcnx" -ln "rgcnx" -at "message";
	addAttr -ci true -sn "sd" -ln "slimData" -dt "string";
	addAttr -ci true -sn "sr" -ln "slimRIB" -dt "string";
	addAttr -ci true -sn "rd" -ln "rlfData" -dt "string";
	setAttr ".sr" -type "string" "";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "renderManRIS";
	setAttr ".outf" 8;
	setAttr ".pram" -type "string" "pgYetiVRayPreRender";
	setAttr ".poam" -type "string" "pgYetiVRayPostRender";
	setAttr ".prlm" -type "string" "pgYetiPrmanFlush";
	setAttr ".polm" -type "string" "pgYetiPrmanFlush";
	setAttr ".prm" -type "string" "";
	setAttr ".pom" -type "string" "pgYetiPrmanFlush";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr ":defaultRenderGlobals.msg" "mtorPartition.rgcnx";
// End of test2.ma
