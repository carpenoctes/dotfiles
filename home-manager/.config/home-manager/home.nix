{ config, pkgs, ... }:

{

  home.username = "saddaf";
  home.homeDirectory = "/home/saddaf";
  home.stateVersion = "23.05"; # Please read the comment before changing.

  # Activate flakes
  nix = {
    package = pkgs.nix;
    settings.experimental-features = [ "nix-command" "flakes" ];
  };


  # Install Nix packages
  home.packages = [
    # pkgs.hello

    # Overrides
    # (pkgs.nerdfonts.override { fonts = [ "FantasqueSansMono" ]; })

    # Simple shell scripts
    # (pkgs.writeShellScriptBin "my-hello" ''
    #   echo "Hello, ${config.home.username}!"
    # '')
  ];



  # Home Manager is pretty good at managing dotfiles. The primary way to manage
  # plain files is through 'home.file'.
  home.file = {
    # # Building this configuration will create a copy of 'dotfiles/screenrc' in
    # # the Nix store. Activating the configuration will then make '~/.screenrc' a
    # # symlink to the Nix store copy.
    # ".screenrc".source = dotfiles/screenrc;

    # # You can also set the file content immediately.
    # ".gradle/gradle.properties".text = ''
    #   org.gradle.console=verbose
    #   org.gradle.daemon.idletimeout=3600000
    # '';
  };

  # You can also manage environment variables but you will have to manually
  # source ~/.nix-profile/etc/profile.d/hm-session-vars.sh or 
  # /etc/profiles/per-user/saddaf/etc/profile.d/hm-session-vars.sh
  # if you don't want to manage your shell through Home Manager.
  home.sessionVariables = {
    # EDITOR = "emacs";
  };

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;
}
