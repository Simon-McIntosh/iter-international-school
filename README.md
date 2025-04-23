# ITER International School Data Science Challenges

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-LGPL--3.0-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![MAST](https://img.shields.io/badge/Data-FAIR--MAST-orange.svg)](https://mastapp.site/)

A collection of Python tools and challenges designed for the 2024 ITER International School in Japan. This project provides access and transformation tools for MAST Tokamak open-source data, forming the basis for three data science challenges.

## Overview

This project uses the Fair-MAST open-source dataset from the Mega Amp Spherical Tokamak (MAST) experiment to create educational challenges for fusion energy data science. The challenges focus on:

1. Plasma current prediction
2. Equilibrium reconstruction
3. Plasma volume estimation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/iter-international-school.git
cd iter-international-school

# Install using Poetry
poetry install
```

## Usage

The package provides tools for accessing and analyzing MAST shot data:

```python
from iter_international_school import mast

# Load a specific shot
shot = mast.Shot(shot_id=29034)

# Access shot data and work with challenges
# TODO provide usage examples with updated API
```

## Data Source

All challenges use the FAIR-MAST dataset, which provides open access to experimental data from the MAST Tokamak at Culham Centre for Fusion Energy. The FAIR-MAST data is accessible at:

- Data Portal: [https://mastapp.site](https://mastapp.site)
- S3 Endpoint: [https://s3.echo.stfc.ac.uk](https://s3.echo.stfc.ac.uk)

## License

This project is licensed under the LGPL-3.0 License - see the LICENSE file for details.

## Author

Simon McIntosh (simon.mcintosh@iter.org)
