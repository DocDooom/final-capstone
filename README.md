# HyperionDev DfE Software Engineering - Capstone Projects
- Created By: <a href="https://www.linkedin.com/in/gabriel-desir/" target="_blank">McZane Gabriel Desir </a>

## Table of Contents
| Name                                                                   | Description                                                                                                             |  Technology  |
|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|---|
| [Shoe Store Inventory Manager](#capstone-project-iv-inventory-manager) | A shoe store inventory manager that allows the user to add, update and view all of the stock in their store's inventory | Python |



---
## [Capstone Project IV: Inventory Manager](#dfe-software-engineering---capstone-projects) 

### Overview
This script allows a user to manage and administrate their stock. In this particular example a shoe store's inventory is included
in the **inventory.txt** file provided. However, any text file containing CSV formatted data can be read by the manager.
To search by SKU a unique SKU identifier must be included.

  <p align="center"><img src="images/capstone_iv_01.PNG"  width="400" target="_blank"/><br><i>Inventory Manager main menu</i></p>

### Files Inclduded
- **inventory.py:** Main program file containing the **Shoes** class and functions to perform various tasks.
- **inventory.txt:** A text file containing the data for the shoe warehouse.

### Getting Started
The following instruction will help you get up and running

#### Prerequisites
You will need the following installed to run the **inventory management tool**
These can either be installed globally or you can create a virtual environment
learn more about virtual environments here

- [How to Set Up a Virtual Environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

The following packages/installs are needed:

- [Python 3](https://www.python.org/)
- [Tabulate](https://pypi.org/project/tabulate/) (for formatting table output)
- [Pandas](https://pypi.org/project/pandas/) (used for handling of CSV data)

#### Installation

1. **Clone** the repository:

```sh
git clone https://github.com/DocDooom/final-capstone.git
```

2. Install Tabulate:

```sh
pip install tabulate
```

3. Install Pandas:

```sh
pip install pandas
```
4. In a Terminal or Command Prompt window **Navigate** to the project directory:

```
cd ./capstone_iv/
```

5. **Run** the **inventory.py** file:

```sh
python inventory.py
```

---

### Usage
To run the program, execute the **inventory.py** file. A menu will be displayed, allowing you to choose which task to perform. Follow the prompts to complete the task.

#### Menu
Once the user accesses the program, the menu is shown below:
- **1** - Check inventory
- **2** - Restock item
- **3** - Search item
- **4** - Inventory value
- **5** - Item being for sale

  <p align="center"><img src="assets/capston04_1.png"  width="600" target="_blank"/><br><i>Fig. 4.2 Menu</i></p>

#### Features

- **Check inventory:** It displays **country**, **product code,** **product name**, **cost** and **quantity** of all the inventory in the warehouse.

  <p align="center"><img src="assets/capston04_2.png"  width="600" target="_blank"/><br><i>Fig. 4.3 Check inventory</i></p>

- **Restock item:** It finds the item with the **lowest** quantity that need to be re-stocked. 

  <p align="center"><img src="assets/capston04_3.png"  width="600" target="_blank"/><br><i>Fig. 4.4 Restock item</i></p>
  
  <p align="center"><img src="assets/capston04_4.png"  width="600" target="_blank"/><br><i>Fig. 4.5 Restock item (+ quantity) </i></p>
 
- **Search item:** It searches for a item by product **code**.

<p align="center"><img src="assets/capston04_5.png"  width="600" target="_blank"/><br><i>Fig. 4.6 Search item by product code</i></p>

-  **Inventory value:** It calculates the total value (**cost x quantity**) for each item.

<p align="center"><img src="assets/capston04_6.png"  width="600" target="_blank"/><br><i>Fig. 4.7 Inventory value</i></p>

- **Item being for sale:** It determines the item with the **highest quantity** as being for sale.

<p align="center"><img src="assets/capston04_7.png"  width="600" target="_blank"/><br><i>Fig. 4.8 Item being for sale</i></p>


---

## Acknowledgments
This project(s) is my solution for tasks created by [HyperionDev](https://www.hyperiondev.com/). 
