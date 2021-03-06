# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

import configparser
import os
import time

prefix = "[SMCSM] » "


def configuration(delete=False):

    configuration.config_version = 1.1

    if delete:
        os.remove('user_config.ini')
    while True:
        try:
            # Search for config and if not found, prompt generation of first time configuration
            print(prefix + "Looking for config: ", end="")
            config = configparser.ConfigParser()
            if len(config.read('user_config.ini')) == 0:
                print("[NO]\n" + prefix + "Generating first time configuration...\n")

                config.add_section('Config')
                config.set('Config', 'Version', str(configuration.config_version))

                config.add_section('Server Settings')
                print(prefix + "Enter your desired ram allocation in GB. (Default is 2.0GB)")
                ram = input(prefix)

                if not ram:
                    config.set('Server Settings', 'Allocated Ram', '2')
                else:
                    config.set('Server Settings', 'Allocated Ram', ram)

                print(prefix + "Disabled auto-start by default. To enable, go to settings.")

                config.add_section('Versions')
                versions = ["1.16.5", "1.16.4", "1.16.3", "1.16.2", "1.16.1", "1.15.2", "1.15.1", "1.15", "1.14.4", "1.14.3", "1.14.2", "1.14.1", "1.14",
                            "1.13.2", "1.13.1", "1.13-pre7", "1.13", "1.12.2", "1.12.1", "1.12", "1.11.2", "1.10.2",
                            "1.9.4", "1.8.8"]

                for version in versions:
                    config.set('Versions', version, '0')

                # config.set('Server Settings', 'Paper Version', '')
                config.set('Server Settings', 'Auto Start', 'false')

                try:
                    ram = "{:.0f}".format(float(ram) * 1000)
                except:
                    ram = "{:.0f}".format(float(2) * 1000)

                optimized_start = f'java ' \
                                  f'-Xms{str(ram)}M ' \
                                  f'-Xmx{str(ram)}M ' \
                                  f'-XX:+UseG1GC ' \
                                  f'-XX:+ParallelRefProcEnabled ' \
                                  f'-XX:MaxGCPauseMillis=200 ' \
                                  f'-XX:+UnlockExperimentalVMOptions ' \
                                  f'-XX:+DisableExplicitGC ' \
                                  f'-XX:-OmitStackTraceInFastThrow ' \
                                  f'-XX:+AlwaysPreTouch ' \
                                  f'-XX:G1NewSizePercent=30 ' \
                                  f'-XX:G1MaxNewSizePercent=40 ' \
                                  f'-XX:G1HeapRegionSize=8M ' \
                                  f'-XX:G1ReservePercent=20 ' \
                                  f'-XX:G1HeapWastePercent=5 ' \
                                  f'-XX:G1MixedGCCountTarget=8 ' \
                                  f'-XX:InitiatingHeapOccupancyPercent=15 ' \
                                  f'-XX:G1MixedGCLiveThresholdPercent=90 ' \
                                  f'-XX:G1RSetUpdatingPauseTimePercent=5 ' \
                                  f'-XX:SurvivorRatio=32 ' \
                                  f'-XX:MaxTenuringThreshold=1 ' \
                                  f'-Dusing.aikars.flags=true ' \
                                  f'-Daikars.new.flags=true ' \
                                  f'-jar server.jar nogui'

                config.set('Server Settings', 'Launch Args', optimized_start)
                config.set('Server Settings', "server jar", "server.jar")
                print(prefix + "Writing config...", end="")

                with open("user_config.ini", "w+") as configfile:
                    config.write(configfile)
                configfile.close()

                print("Done. \n" + prefix + "Refreshing...\n")
                continue

            else:
                try:
                    config = configparser.ConfigParser()
                    config.read('user_config.ini')
                    configuration.current_config_version = config['Config']['Version']

                    if float(configuration.current_config_version) < configuration.config_version:
                        configuration.config_status = "Update here!"
                        print("[OUT OF DATE]")
                    else:
                        configuration.config_status = "Up to Date!"
                        print("[OK]")

                except KeyError:
                    print("[VERSION ERROR: Is config file old?]")
                    configuration.config_status = "Out of Date!"

                configuration.ram = config['Server Settings']['Allocated Ram']
                configuration.optimized_start = config['Server Settings']['Launch Args']
                break

        except KeyError:
            print(prefix + "KeyError: Could not grab configuration from file. "
                           f"Deleting broken config...", end="")
            os.remove("user_config.ini")
            print("Done!\n" + prefix + "Restarting...")
            time.sleep(0.75)
            continue
