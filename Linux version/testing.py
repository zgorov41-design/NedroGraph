        if settings_c and rgb11:
            if event.type == pygame.TEXTINPUT:
                if len(text11) < 3 and event.text.isdigit():
                    text11 += event.text

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text11 = text11[:-1]

                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if text11.strip() != "":
                        print("Value:", text11)
                        rgb11 = False
                        colors.panel["r"] = int(text11)
                        print(text11)

                        config_file = Path("colors.py")
                        config_text = config_file.read_text(encoding="utf-8")
                        lines = config_text.splitlines()
                        for i, line in enumerate(lines):
                            if line.strip().startswith("panel ="):
                                lines[i] = re.sub(r'("r"\s*:\s*)\d+', rf'\g<1>{text11}', line)
                                break
                        config_file.write_text("\n".join(lines) + "\n", encoding="utf-8")