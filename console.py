#!/usr/bin/env python3
"""
A Command-line interpreter for GroceryHub
"""
from os import getenv
import re
import ast
import cmd
import sys
import shlex
import code
from models import storage
from models.base_model import BaseModel
from models.product import Product
from models.order import Order
from models.shop import Shop
from models.category import Category
from models.place import Place
from models.user import User
from models.shop_list import Shop_list


class GroceryHubCLI(cmd.Cmd):
    """Command line interpreter for GroceryHub"""
    intro = (
        "GroceryHub Command-line interpreter.\n"
        "\nRules:\n"
        "  Each argument should be separated by a space\n"
        "  String arguments with spaces must be double quoted\n"
        "\nType shell or ! to access python3 interpreter"
        "\nType help or ? to list commands.\n"
        "\nNote: Use ctrl + d to exit python3 interpreter\n"
    )
    prompt = "(GroceryHub) " if sys.__stdin__.isatty() else ''

    cls_lst = {
            "BaseModel": BaseModel,
            "Product": Product,
            "Order": Order,
            "Shop": Shop,
            "Category": Category,
            "Place": Place,
            "User": User,
            "Shop_list": Shop_list
            }
    class_list = list(cls_lst)

    def preloop(self):
        """Format for non-interactive session"""
        if not sys.__stdin__.isatty():
            self.intro = ''
            print("(GroceryHub) ", end='')

    def postloop(self):
        """Format for non-interactive session"""
        if not sys.__stdin__.isatty():
            print("(GroceryHub)")

    def param_parser(self, args):
        """Creates a dictionary from a list of key-value args"""
        new_dict = {}
        for arg in args:
            if '=' in arg:
                params = arg.split('=', 1)
                key = params[0]
                val = params[1]

                if val[0] == val[-1] == '"':
                    val = val[1:-1].replace('_', ' ')
                    val = re.sub(r'\\"', '"', val)

                elif val.isdigit():
                    val = int(val)

                elif '.' in val:
                    try:
                        val = float(val)
                    except ValueError:
                        pass

                new_dict[key] = val
        return new_dict

    def start_python_interpreter(self):
        """Starts an interactive Python interpreter"""
        # Copy global variables to the local scope
        local_vars = globals().copy()
        local_vars.update(locals())  # Include local variables

        # Start the interactive interpreter
        interpreter = code.InteractiveConsole(locals=local_vars)
        interpreter.interact(
            "Python 3 interactive interpreter. Type Ctrl-D to return."
                )

    def do_shell(self, arg):
        """Execute a Python interpreter command"""
        self.start_python_interpreter()
        print(
            "Exiting the Python interpreter. "
            "Returning to the GroceryHub CLI."
        )

    def do_create(self, arg):
        """Creates and saves a new instance of a class model"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        if args[0] in self.cls_lst:
            cls = self.cls_lst[args[0]]
            new_dict = self.param_parser(args[1:])
            inst = cls(**new_dict)
            inst.save()
            print(inst.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Displays an instance representation"""
        args = shlex.split(arg)

        if args:
            if args[0] in self.cls_lst:
                if len(args) == 1:
                    print("** instance id missing **")
                else:
                    cls = self.cls_lst[args[0]]
                    key = f"{args[0]}.{args[1]}"
                    print(
                        storage.all(cls).get(
                            key,
                            "** no instance found **"
                        )
                    )
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_destroy(self, arg):
        """Deletes an instance"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")

        elif args[0] in self.cls_lst:
            if len(args) == 1:
                print("** instance id missing **")
            else:
                cls = self.cls_lst[args[0]]
                obj = storage.get(cls, args[1])

                if obj:
                    obj.delete()
                    storage.save()
                else:
                    print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """List all instance of a class or of all classes"""
        args = shlex.split(arg)
        objs = []

        if not args:
            stored_dict = storage.all()
            objs = [str(obj) for obj in stored_dict.values()]
            print(objs)

        elif args[0] in self.cls_lst:
            stored_dict = storage.all(self.cls_lst[args[0]])
            objs = [str(obj) for obj in stored_dict.values()]
            print(objs)

        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance's attributes"""
        # Handles dict interpretation
        arg = arg.replace("'", '"')
        arg = arg.replace('{', "'{")
        arg = arg.replace('}', "}'")

        args = shlex.split(arg)

        if not args:
            print("** class name missing **")

        elif args[0] in self.cls_lst:
            if len(args) == 1:
                print("** instance id missing **")
            else:
                cls = self.cls_lst[args[0]]
                obj = storage.get(cls, args[1])

                if obj:
                    if len(args) == 2:
                        print("** attribute name missing **")
                    else:
                        # safe conversion of str to python datatype
                        excld = ["id", "created_at", "updated_at"]
                        if args[2] in excld:
                            print("** this attribute can't be updated **")
                            return
                        try:
                            args[2] = ast.literal_eval(args[2])
                        except (ValueError, SyntaxError) as e:
                            pass

                        if len(args) == 3 and not isinstance(args[2], dict):
                            print("** value missing **")

                        elif isinstance(args[2], dict):
                            for ky, val in args[2].items():
                                setattr(obj, ky, val)
                            obj.save()
                        else:
                            setattr(obj, args[2], args[3])
                            obj.save()
                else:
                    print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_count(self, arg):
        """Get the number of all or certain class instances"""
        args = shlex.split(arg)

        if not args:
            print(storage.count())

        elif args[0] in self.cls_lst:
            print(storage.count(args[0]))

        else:
            print("** class doesn't exist **")

    def do_link(self, arg):
        """Link product instances to a shop_list instance."""
        args = shlex.split(arg)

        if not args:
            print("** Shop_list class name missing ***")
        elif args[0] in self.cls_lst:
            if args[0] != "Shop_list":
                print("** parent class name should be Shop_list **")
                return

            if len(args) < 2:
                print("** Shop_list instance id missing **")
            else:
                shop_list = storage.get(
                        self.cls_lst[args[0]],
                        args[1]
                        )

                if not shop_list:
                    print("** Shop_list instance not found **")
                    return

                if len(args) < 3:
                    print("** child class name missing **")
                    return

                if args[2] not in self.cls_lst or args[2] != "Product":
                    print("** child class name should be Product **")
                    return

                if len(args) < 4:
                    print("** product instance(s) id missing **")
                    return

                product_ids = args[3:]

                if not product_ids:
                    return

                for product_id in product_ids:
                    try:
                        shop_list.set_product_qty(product_id)
                    except ValueError:
                        print(f"** Product instance {product_id} not found **")
                shop_list.save()
        else:
            print("** parent class doesn't exist **")

    def do_make_order(self, arg):
        """Create order instances from shop_list instance"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")

        elif args[0] in self.cls_lst:
            if args[0] != "Shop_list":
                print("** class name should be Shop_list **")
                return

            if len(args) == 1:
                print("** instance id missing **")
            else:
                cls = self.cls_lst[args[0]]
                shop_list = storage.get(cls, args[1])

                if shop_list:
                    orders = shop_list.make_order()
                    print(
                        "\n".join(
                            [order.id for order in orders])
                    )
                else:
                    print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_add_product_qty(self, arg):
        """Updates a product quantity in a shop_list instance"""
        args = shlex.split(arg)

        if not args:
            print("** Shop_list class name missing ***")
        elif args[0] in self.cls_lst:
            if args[0] != "Shop_list":
                print("** parent class name should be Shop_list **")
                return

            if len(args) < 2:
                print("** Shop_list instance id missing **")
            else:
                shop_list = storage.get(
                        self.cls_lst[args[0]],
                        args[1]
                        )
                if shop_list:
                    if len(args) < 3:
                        print("** child class name missing **")
                        return

                    if args[2] not in self.cls_lst:
                        print("** child class doesn't exist **")
                        return

                    if args[2] != "Product":
                        print("** child class name should be Product **")
                        return

                    if len(args) < 4:
                        print("** product instance id missing **")
                        return

                    if len(args) < 5:
                        print("** product quantity missing **")
                        return

                    if not args[4].isdigit():
                        print("** quantity should be a digit **")
                        return

                    qty = int(args[4])
                    if qty <= 0:
                        print(
                            "** quantity should be a positive number **"
                        )
                        return
                    try:
                        shop_list.set_product_qty(args[3], qty)
                    except ValueError:
                        print("** product_id not found **")
                        return
                    shop_list.save()
                else:
                    print("** Shop_list instance not found **")
        else:
            print("** parent class doesn't exist **")

    def do_build_list(self, arg):
        """Create shop_list instances from a user instance"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")

        elif args[0] in self.cls_lst:
            if args[0] != "User":
                print("** class name should be User **")
                return

            if len(args) == 1:
                print("** instance id missing **")
            else:
                cls = self.cls_lst[args[0]]
                user = storage.get(cls, args[1])

                if user:
                    new_list = user.make_shop_list()
                    print(new_list.id)
                else:
                    print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_quit(self, arg):
        """Exits the program"""
        return True

    do_exit = do_quit

    def header(self, command, id=False):
        print("\nArguments:")
        print("  <class_name>  The name of the class instance")
        if id:
            print("  <id>          The id of the class instance")
        if command != "create":
            print("  [...]         Optional argument")
        print("\nUsage:")
        if not id:
            if command == "create":
                print(f"  {command} <class_name> keyword=\"value\"...")
            else:
                print(f"  {command} [<class_name>]")
            print(f"  <class_name>.{command}()\n")

        else:
            print(f"  {command} <class_name> <id>")
            print(f"  <class_name>.{command}(<id>)\n")

        print("Available classes:")
        for cls in self.cls_lst:
            print(f"  {cls}")

    def help_create(self):
        print("\nCreate and saves new instance of a class model")
        print("================================================")
        self.header("create")
        print()

    def help_destroy(self):
        print("\nDeletes an instance of a class model")
        print("======================================")
        self.header("destroy", id=True)
        print()

    def help_show(self):
        print("\nDisplays the details of an instance of a class model")
        print("======================================================")
        self.header("show", id=True)
        print()

    def help_all(self):
        print("\nDisplays the details of all instances of all class models")
        print("===========================================================")
        self.header("all")
        print()

    def help_update(self):
        print("\nUpdates the attributes of an instance of a class model")
        print("========================================================")
        print("\nUsage:")
        print("  update <class_name> <id> <attribute_name> <new_value>")
        print("  <class_name>.update(<id>, <attribute_name>, <new_value>)\n")
        print("Arguments:")
        print("  <class_name>      The name of the class instance to update")
        print("  <id>              The id of the class instance to update")
        print("  <attribute_name>  The name of the attribute to update")
        print("  <new_value>       The new value for the attribute\n")
        print("Examples:")
        print("  update User name John")
        print("  User.update(name, John)")
        print("\nAvailable classes:")
        for cls in self.cls_lst:
            print(f"  {cls}")
        print()

    def help_count(self):
        print("\nDisplays the number of instances of a class model")
        print("===================================================")
        self.header("count")
        print()

    def help_link(self):
        print("\nLink product instances to a shop_list instance")
        print("================================================")
        print("\nUsage:")
        print(
                "  link <Shop_list> <shop_list_id> "
                "<Product> <product_id1> [<product_id2> ...]"
        )
        print(
                "  <Shop_list>.link(<id>, <Product>, "
                "<product_id1> [<product_id2> ...])\n"
        )
        print("Arguments:")
        print("  <Shop_list>          The Shop_list class name")
        print(
                "  <shop_list_id>       "
                "The Shop_list instance id to link products to"
        )
        print("  <Product>            The Product class name")
        print(
                "  <product_id1>        "
                "The Product instance id to be linked to Shop_list instance"
        )
        print(
                "  [<product_id2> ...]  Optional: "
                "additional Product instance IDs to link\n"
        )
        print("Examples:")
        print("  - To link a single product to a shop_list:")
        print("       link Shop_list 1234 Product 5678")
        print("       Shop_list.link(1234, Product, 5678)\n")
        print("  - To link multiple products to a shop_list:")
        print("       link Shop_list 1234 Product 05678 91011 121314")
        print("       Shop_list.link(1234, Product, 05678, 91011, 121314)\n")

    def help_make_order(self):
        print("\n Creates orders from a shop_list instance")
        print("===========================================")
        print("\nUsage:")
        print("  make_order <Shop_list> <shop_list_id>")
        print("  <Shop_list>.make_order(<shop_list_id>)\n")
        print("Arguments:")
        print("  <Shop_list>     The Shop_list class name")
        print(
                "  <shop_list_id>  "
                "The Shop_list instance id to create orders from\n"
        )
        print("Examples:")
        print("  make_order Shop_list 1234")
        print("  Shop_list.make_order(1234)\n")

    def help_add_product_qty(self):
        print("\nUpdates a product quantity in a shop_list instance")
        print("====================================================")
        print("\nUsage:")
        print(
                "  add_product_qty <Shop_list> <shop_list_id> "
                "<Product> <product_id1> <quantity>"
        )
        print(
                "  <Shop_list>.add_product_qty(<id>, <Product>, "
                "<product_id1> <quantity)\n"
        )
        print("Arguments:")
        print("  <Shop_list>          The Shop_list class name")
        print(
                "  <shop_list_id>       "
                "The Shop_list instance products to update"
        )
        print("  <Product>            The Product class name")
        print(
                "  <product_id1>        "
                "The Product instance id to be updated"
        )
        print(
                "  <quantity>           "
                "Quantity of product to add to shop_list\n"
        )
        print("Examples:")
        print("  add_product_qty Shop_list 1234 Product 5678 5")
        print("  Shop_list.add_product_qty(1234, Product, 5678, 5)\n")
        print("Note:")
        print(
            "  Passing zero or a negative number as quantity "
            "would throw an error\n"
        )

    def help_build_list(self):
        print("\n Creates shop_list from a user instance")
        print("===========================================")
        print("\nUsage:")
        print("  build_list <User> <user_id>")
        print("  <User>.build_list(<user_id>)\n")
        print("Arguments:")
        print("  <User>     The User class name")
        print(
                "  <user_id>  "
                "The User instance id to create shop_list from\n"
        )
        print("Examples:")
        print("  build_list User 1234")
        print("  User.build_list(1234)\n")

    def complete_command(self, text, line, begidx, endidx, command):
        """Common completion method for class-based commands"""
        if not text:
            completions = self.class_list[:]
        else:
            completions = [cls + ' ' for cls in self.class_list
                           if cls.startswith(text)]
        return completions

    def complete_create(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'create')

    def complete_destroy(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'destroy')

    def complete_show(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'show')

    def complete_all(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'all')

    def complete_update(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'update')

    def complete_count(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'count')

    def complete_link(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'link')

    def complete_make_order(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'make_order')

    def complete_add_product_qty(self, text, line, begidx, endidx):
        return self.complete_command(
                text, line, begidx, endidx, 'add_product_qty')

    def complete_build_list(self, text, line, begidx, endidx):
        return self.complete_command(text, line, begidx, endidx, 'build_list')

    def precmd(self, arg):
        """Handles commands calls using <class_name>.command()"""
        if '.' in arg:
            # Extract command and arguments
            parts = arg.split('.', maxsplit=1)
            cls_name, cmd_parts = parts[0], parts[1].split('(')
            cmd = cmd_parts[0]

            if cls_name not in self.cls_lst:
                return arg

            # Processing for dictionary arguments
            if '{' in cmd_parts[1]:
                cmd_args = cmd_parts[1].split('{')
                id_arg = cmd_args[0].strip()
                id_arg = id_arg.rstrip(',')
                dict_arg = '{' + cmd_args[1].rstrip(')')

                rebuilt_arg = f"{cmd} {cls_name} {id_arg} {dict_arg}"

                return rebuilt_arg

            # Extract the argument from within parentheses (if present)
            if len(cmd_parts) > 1:
                # Remove trailing parenthesis
                raw_args = cmd_parts[1].rstrip(')')

                # Process raw string args to remove delimiters like ','
                list(raw_args)
                args = "".join(char for char in raw_args if char != ',')
            else:
                args = None

            # Rebuild the command and return it for processing
            if args:
                rebuilt_cmd = f"{cmd} {cls_name} {args}"
            else:
                rebuilt_cmd = f"{cmd} {cls_name}"
            return rebuilt_cmd

        else:
            return arg  # Return original argument

    def emptyline(self):
        """Overrides default emptyline response"""
        pass


if __name__ == "__main__":
    GroceryHubCLI().cmdloop()
