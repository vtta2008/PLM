//Maya ASCII 2017ff04 scene
//Name: test4.ma
//Last modified: Sun, May 14, 2017 11:23:46 AM
//Codeset: 1252
requires maya "2017ff04";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201702071345-1015190";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "Four_Sides_Arrow";
	rename -uid "FB1F2BC6-44B9-B6BF-0916-4FAC6EB29D60";
createNode nurbsCurve -n "Four_Sides_ArrowShape" -p "Four_Sides_Arrow";
	rename -uid "19AA9C83-41F2-7F3E-359B-4C86EEC07204";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 7 0 no 3
		8 0 1 2 3 4 5 6 7
		8
		-2 0 0
		1 0 1
		1 0 -1
		-2 0 0
		1 1 0
		1 0 0
		1 -1 0
		-2 0 0
		;
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
// End of test4.ma
