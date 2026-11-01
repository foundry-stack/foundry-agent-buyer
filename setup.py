import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="foundry-agent-buyer",
    version="1.0.0",
    author="Foundry Stack",
    author_email="orders@foundrystack.co.uk",
    description="Zero-config Python client for autonomous AI agents to buy digital goods via HTTP 402 on Base and Avalanche",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/foundry-stack/foundry-agent-buyer",
    project_urls={
        "Commercial Infrastructure": "https://foundrystack.co.uk",
        "Bug Tracker": "https://github.com/foundry-stack/foundry-agent-buyer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    py_modules=["foundry_agent_buyer"],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "web3>=6.0.0",
        "eth-account>=0.10.0"
    ],
)
