# -*- coding: utf-8 -*-
import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer
from testwindow import show_test_window

def main():
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    io = imgui.get_io()
    io.config_flags |= imgui.CONFIG_VIEWPORTS_ENABLE | imgui.CONFIG_DOCKING_ENABLE 
    show_custom_window = True
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()
        viewport = imgui.get_main_viewport()
        imgui.set_next_window_position(viewport.pos.x, viewport.pos.y)
        imgui.set_next_window_size(viewport.size[0], viewport.size[1])
        imgui.set_next_window_viewport(viewport.id)
        imgui.set_next_window_bg_alpha(0.0)
        window_flags = imgui.WINDOW_MENU_BAR|imgui.WINDOW_NO_DOCKING
        window_flags |= imgui.WINDOW_NO_TITLE_BAR|imgui.WINDOW_NO_COLLAPSE|imgui.WINDOW_NO_RESIZE
        window_flags |= imgui.WINDOW_NO_MOVE|imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS|imgui.WINDOW_NO_NAV_FOCUS

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING,(0.0,0.0))
        imgui.begin("Dockspace Demo", 0, window_flags)
        imgui.pop_style_var()
        imgui.pop_style_var()
        imgui.pop_style_var()
 
        flags = imgui.DOCK_NODE_PASS_THRU_CENTRAL_NODE
        id = imgui.get_id('MyDockspace')
        imgui.dockspace(id, flags=flags)
        if show_custom_window:
            is_expand, show_custom_window = imgui.begin("Custom window", True, )
            if is_expand:
                imgui.text("Bar")
                imgui.text_ansi("B\033[31marA\033[mnsi ")
                imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)
                imgui.extra.text_ansi_colored("Eggs", 0.2, 1., 0.)
            imgui.end()

        # show_test_window()
        imgui.show_test_window()
        imgui.end()
        gl.glClearColor(.1, .1, .1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


if __name__ == "__main__":
    main()
