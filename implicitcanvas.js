class ImplicitCanvas extends SimpleMeshCanvas {

    /**
     * @param {DOM Element} glcanvas Handle to HTML where the glcanvas resides
     * @param {string} shadersrelpath Path to the folder that contains the shaders,
     *                                relative to where the constructor is being called
     * @param {string} editorName Name of the javascript editor for the height function
     */
    constructor(glcanvas, shadersrelpath, editorName) {
        // Setup GL Canvas
        super(glcanvas, shadersrelpath);
        const that = this;
        // Setup editor
        this.mainEditor = ace.edit(editorName);
        this.mainEditor.setFontSize(16);
        // Setup new parts of menu
        this.setupISOMenu();
        this.updateVolume();
    }

    /**
     * Add options for the heightmap, including resolution and isolevel
     */
    setupISOMenu() {
        const that = this;
        let gui = this.gui;
        let igui = gui.addFolder("Isocontour Options");
        this.igui = igui;
        this.res =  50;
        igui.add(this, "res", 5, 200);
        igui.add(this, "updateVolume");
        this.isolevel = 0.5;
        this.isochooser = igui.add(this, "isolevel", 0, 1);
        igui.add(this, "updateIsocontours");
    }

    updateIsocontours() {
        this.mcubes.triangulate(this.isolevel);
        let mesh = new BasicMesh();
        let vertices = this.mcubes.vertices;
        let tris = this.mcubes.tris;
        console.log(vertices);
        console.log(tris);
        for (let i = 0; i < vertices.length; i++) {
            let v = vertices[i];
            mesh.addVertex(glMatrix.vec3.fromValues(v[0], v[1], v[2]));
        }
        for (let i = 0; i < tris.length; i++) {
            let tri = tris[i];
            mesh.addFace([mesh.vertices[tri[0]],
                          mesh.vertices[tri[1]],
                          mesh.vertices[tri[2]]]);
        }
        this.mesh.vertices = mesh.vertices;
        this.mesh.edges = mesh.edges;
        this.mesh.faces = mesh.faces;
        this.mesh.needsDisplayUpdate = true;
        this.centerCamera();
        requestAnimationFrame(this.repaint.bind(this));
    }

    updateVolume() {
        let gui = this.igui;
        const that = this;
        try {
            let s = this.mainEditor.getValue();
            s += "return fn(arguments[0], arguments[1], arguments[2]);";
            this.fn = new Function(s);
            this.mcubes = new MarchingCubes(this.fn, this.res);
            let dx = (this.mcubes.max-this.mcubes.min)/100;
            this.isolevel = 0.5*(this.mcubes.min+this.mcubes.max);
            gui.remove(this.isochooser);
            this.isochooser = gui.add(this, "isolevel", this.mcubes.min, this.mcubes.max, dx);
            this.updateIsocontours();
        }
        catch (err) {
            alert("Javascript syntax error! Check console");
            throw err;
        }
    }


    repaint() {
        this.gl.viewport(0, 0, this.gl.viewportWidth, this.gl.viewportHeight);
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
        this.lights = [{pos:this.camera.pos, color:[1, 1, 1], atten:[1, 0, 0]}];
        let canvas = this;
        if (!('shaderReady' in this.shaders.blinnPhong)) {
            // Wait until the promise has resolved, then draw again
            this.shaders.blinnPhong.then(canvas.repaint.bind(canvas));
        }
        else {
            this.shaderToUse = this.shaders.blinnPhong;
            this.mesh.render(this);
        }
    };
}