import omni.ext
import omni.ui as ui
import omni.usd

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class NewtonCradleExampleExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[newton.cradle.example] newton cradle example startup")

        self._count = 0

        self._window = ui.Window("Script Anim Physics", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                with ui.HStack(height = 20):
                    ui.Button("Add force", clicked_fn=self.add_force)

    
    def add_force(self):
        print("Add force")

        import omni.timeline
        from pxr import PhysxSchema, UsdGeom, Gf
        stage = omni.usd.get_context().get_stage()
        omni.timeline.get_timeline_interface().set_end_time(10000/24)

        xform = UsdGeom.Xform.Define(stage, "/World/ball1_04/Xform_01/ballForce")
        forceApi = PhysxSchema.PhysxForceAPI.Apply(xform.GetPrim()) 

        forceAttr = forceApi.GetForceAttr()
        forceAttr.Set(time=0, value=Gf.Vec3f(0.0, 0, 8000.0))
        forceAttr.Set(time=5, value=Gf.Vec3f(0.0, 0, 0))       

        forceEnabledAttr = forceApi.GetForceEnabledAttr()
        forceEnabledAttr.Set(time=0, value=True)
        forceEnabledAttr.Set(time=5, value=False)
        
        # xformable = UsdGeom.Xformable(xform.GetPrim()) 
        # translateOp = xformable.AddTranslateOp()
        # translateOp.Set(time=0, value = Gf.Vec3d(0.0, 0, 0))        
        # translateOp.Set(time=50, value = Gf.Vec3d(0.0, 0, 0))   


    def on_shutdown(self):
        print("[newton.cradle.example] newton cradle example shutdown")
