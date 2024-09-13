{
  "variables": {
    'openssl_fips': ''
  },
  "targets": [{
    "target_name": "classic_level",
    "conditions": [
      ["OS == 'win'", {
        "defines": [
          "_HAS_EXCEPTIONS=0",
          "DLLX=__declspec(dllexport)"
        ],
        "msvs_settings": {
          "VCCLCompilerTool": {
            "RuntimeTypeInfo": "false",
            "EnableFunctionLevelLinking": "true",
            "ExceptionHandling": "2",
            "DisableSpecificWarnings": [ "4355", "4530" ,"4267", "4244", "4506" ]
          }
        }
      }],
      ["OS == 'linux'", {
        "defines": [
          "DLLX="
        ],
        "cflags": [],
        "cflags!": [ "-fno-tree-vrp"]
      }],
      ["OS == 'mac'", {
        "defines": [
          "DLLX="
        ],
        "cflags+": ["-fvisibility=hidden"],
        "xcode_settings": {
          # -fvisibility=hidden
          "GCC_SYMBOLS_PRIVATE_EXTERN": "YES",

          # Set minimum target version because we're building on newer
          # Same as https://github.com/nodejs/node/blob/v10.0.0/common.gypi#L416
          "MACOSX_DEPLOYMENT_TARGET": "10.7",

          # Build universal binary to support M1 (Apple silicon)
          "OTHER_CFLAGS": [
            "-arch x86_64",
            "-arch arm64"
          ],
          "OTHER_LDFLAGS": [
            "-arch x86_64",
            "-arch arm64"
          ]
        }
      }],
      ["OS == 'android'", {
        "defines": [
          "DLLX="
        ],
        "cflags": [ "-fPIC" ],
        "ldflags": [ "-fPIC" ],
        "cflags!": [
          "-fno-tree-vrp",
          "-mfloat-abi=hard",
          "-fPIE"
        ],
        "ldflags!": [ "-fPIE" ]
      }],
      ["target_arch == 'arm'", {
        "defines": [
          "DLLX="
        ],
        "cflags": [ "-mfloat-abi=hard" ]
      }]
    ],
    "dependencies": [
      "<(module_root_dir)/deps/leveldb/leveldb.gyp:leveldb"
    ],
    "include_dirs"  : [
      "<!(node -e \"require('napi-macros')\")"
    ],
    "sources": [
      "binding.cc"
    ]
  }]
}
