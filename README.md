# Conan package recipe for [liblava](https://liblava.dev)

liblava is a modern C++ and easy-to-use library for the Vulkan® API

<br />

# Build and package

The following command will build liblava and publish the Conan package to the local system cache:

```bash
conan create .
```

## Config

It's possible that you need to configure Conan to use your preferred compiler and build settings. For example, to compile a release build with Clang you could use the following config:

```ini
include(default)

[settings]
compiler=clang
compiler.version=13
compiler.cppstd=20
build_type=Release

[env]
CC=clang-13
CXX=clang++
```

Save it as *config_clang* and create the package:

```bash
conan create . -pr=config_clang
```

For more profile configuration options, refer to the [Conan docs](https://docs.conan.io/en/latest/reference/profiles.html).

<br />

# Usage

Add a dependency to liblava to your project's *conanfile.txt*:

```ini
[requires]
liblava/0.8.0@lavablock/stable
```

and install all requirements:

```bash
mkdir build
cd build
conan install ..
```

For more information, refer to [Using packages](https://docs.conan.io/en/latest/using_packages.html).

<br />

# Options

The following options can be configured:

| Option  | Description                          | Default |
|---------|--------------------------------------|---------|
| fPIC    | Generate position-independent code   | True    |
| test    | Build and install lava test binaries | False   |
| demo    | Build and install lava demo binaries | False   |

For information on how to set them, refer to [Options](https://docs.conan.io/en/latest/using_packages/conanfile_txt.html#options).

<br />

# New version

To add a new [tagged lava version](https://github.com/liblava/liblava/tags):

1. Modify conanfile.py
    - update version field
    - if necessary, adapt to any changes to lava's build system
2. Modify README.md
    - update version in Usage / requires section
4. Push to *latest* branch
5. Create new branch *stable/%version%* from *latest*

<br />

<br />

<a href="https://liblava.dev"><img src="https://github.com/liblava.png" width="50"></a>
