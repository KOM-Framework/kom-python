

class AppiumForMac:
    @classmethod
    def get_capabilities(cls, extensions: None):
        defaultLoopDelay_sec = 1.0
        defaultCommandDelay_sec = 0.1
        defaultImplicitTimeout_sec = 1.0
        defaultMouseSpeed = 100
        defaultScreenShotOnError = False
        defaultGlobalDiagnosticsDirectory = '~/Desktop/'
        defaultCookies = [
            {'name': 'loop_delay', 'value': defaultLoopDelay_sec},
            {'name': 'command_delay', 'value': defaultCommandDelay_sec},
            {'name': 'implicit_timeout', 'value': defaultImplicitTimeout_sec},
            {'name': 'mouse_speed', 'value': defaultMouseSpeed},
            {'name': 'screen_shot_on_error', 'value': defaultScreenShotOnError},
            {'name': 'global_diagnostics_directory', 'value': defaultGlobalDiagnosticsDirectory}
        ]
        desiredCapabilities = {'platform': 'Mac', 'cookies': defaultCookies}
        return desiredCapabilities
