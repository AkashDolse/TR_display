from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
import base64
import json
import cv2
import psycopg2
from psycopg2 import sql
import logging
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

# Database path
  # self.conn = psycopg2.connect(
        #     database="postgres",
        #     user="postgres",
        #     host='192.168.88.192',
        #     password="postgres123",
        #     port=5432
        # )


# # --------------------------- Database connection and management ----------------------------------
# class DatabaseConnection:
#     def __init__(self,table_name,tr_type):
#         """
#         Initializes the database connection.
#         """
      
#         self.conn = psycopg2.connect(
#             database="postgres",
#             user="postgres",
#             host='localhost',
#             password="postgres",
#             port=5432
#         )
#         self.cursor = self.conn.cursor()
#         self.table_name = table_name
#         self.tr_type=tr_type
#         self.column_list=["filename","Slicename"]
#         for i in range(1,self.tr_type+1):
#             self.column_list.append(f"Column_{i}")
#         # print(self.column_list)
    
    
#     # def setup_table(self, table_name, tr_column):
#     #     """
#     #     Creates a table with the specified number of columns.
#     #     """
#     #     print(table_name, tr_column)
#     #     columns = ["filename TEXT", "Slicename TEXT"] + [f"Column_{i} TEXT" for i in range(1, tr_column + 1)]
#     #     columns_str = ", ".join(columns)
#     #     query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
#     #         sql.Identifier(table_name),
#     #         sql.SQL(columns_str)
#     #     )
#     #     self.cursor.execute(query)
#     #     self.conn.commit()

#     def setup_table(self, table_name, tr_column):
#         """
#         Creates a table with the specified number of columns.
#         """
#         print("Under Set up table")
#         # print(table_name, tr_column)
#         # Generate the column definitions
#         columns = [
#             sql.SQL("{} TEXT").format(sql.Identifier("filename")),
#             sql.SQL("{} TEXT").format(sql.Identifier("Slicename"))
#         ] + [
#             sql.SQL("{} TEXT").format(sql.Identifier(f"Column_{i}")) for i in range(1, tr_column + 1)
#         ]

#         # Combine column definitions into a single SQL object
#         columns_str = sql.SQL(", ").join(columns)

#         # Construct the CREATE TABLE query
#         query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
#             sql.Identifier(table_name),
#             columns_str
#         )

#         # Execute the query
#         self.cursor.execute(query)
#         self.conn.commit()


#     def insert_data(self, filename, table_name, slice_name, data, tr_column):
#         """
#         Inserts or updates a row of data in the table.
        
#         """
#         print("Under Insert Data")
#         # print("\n\n\n",data)
#         # print(filename, table_name, slice_name, data, tr_column)

#         if not isinstance(tr_column, int):
#             raise ValueError("tr_column must be an integer representing the number of additional columns.")
        
#         if len(data) != tr_column:
#             raise ValueError(f"Expected {tr_column} data elements, but got {len(data)}.")

#         # Check if slice_name exists
#         check_query = sql.SQL("SELECT 1 FROM {} WHERE {} = %s").format(
#             sql.Identifier(table_name),  # Ensures the table name is quoted
#             sql.Identifier("Slicename") # Ensures the column name is quoted
#         )
#         self.cursor.execute(check_query, (slice_name,))
#         exists = self.cursor.fetchone()

#         print("-"*20,"Line 118")

#         # if exists:
#         #     # Update existing row
#         #     print("-"*20,"Line 122")
#         #     update_columns = [f"Column_{i} = %s" for i in range(1, tr_column + 1)]
#         #     print(update_columns)
#         #     update_query = sql.SQL(
#         #         "UPDATE {} SET {}, filename = %s WHERE {} = %s"
#         #         ).format(
#         #             sql.Identifier(table_name),
#         #             sql.SQL(", ").join(
#         #                 sql.SQL("{} = %s").format(sql.Identifier(column)) for column in update_columns
#         #             ),
#         #             sql.Identifier("Test45_correction.Slicename")  # Properly quoting Slicename
#         #     )

#         #     self.cursor.execute(update_query, data + [filename, slice_name])
#         #     print(f"Updated row for Slicename: {slice_name}")
       
#         if exists:
#             # Update existing row
#             print("-"*20, "Line 122")
#             update_columns = [f"Column_{i} = %s" for i in range(1, tr_column + 1)]
#             print(update_columns)
#             update_query = sql.SQL(
#                 "UPDATE {} SET {}, filename = %s WHERE {} = %s"
#             ).format(
#                 sql.Identifier(table_name),
#                 sql.SQL(", ").join(
#                     sql.SQL("{} = %s").format(sql.Identifier(f"Column_{i}")) for i in range(1, tr_column + 1)
#                 ),
#                 sql.Identifier("Slicename")  # Correctly quoting Slicename
#             )

#             self.cursor.execute(update_query, data + [filename, slice_name])
#             print(f"Updated row for Slicename: {slice_name}")

#         else:
#             # Insert new row
#             print("-"*20,"Line 138")
#             columns = ["filename", "Slicename"] + [f"Column_{i}" for i in range(1, tr_column + 1)]
#             placeholders = ", ".join(["%s"] * len(columns))
#             insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
#                 sql.Identifier(table_name),
#                 sql.SQL(", ").join(map(sql.Identifier, columns)),
#                 sql.SQL(placeholders)
#             )
#             self.cursor.execute(insert_query, [filename, slice_name] + data)
#             print(f"Inserted new row for slice_name: {slice_name}")
        
#         self.conn.commit()

#     def fetch_data(self, column, row_number, table_name):
#         """
#         Fetches data from the specified table and column at a given row.
#         """
#         print("under fetch _data code")
#         try:
#             # query = sql.SQL(f"SELECT {', '.join(self.column_list)} FROM {} OFFSET %s LIMIT 1").format(sql.Identifier(self.table_name))
#             query = sql.SQL(
#                             "SELECT {columns} FROM {table} OFFSET %s LIMIT 1"
#                             ).format(
#                             columns=sql.SQL(', ').join(map(sql.Identifier, self.column_list)),
#                             table=sql.Identifier(self.table_name)
#                         )

#             self.cursor.execute(query, (row_number,))
#             result = self.cursor.fetchone()
#             # print(result)
#             return result
#         except psycopg2.Error as e:
#             print(f"An error occurred: {e}")
#             return None

#     def close(self):
#         """
#         Closes the database connection.
#         """
#         self.cursor.close()
#         self.conn.close()


# --------------------------- Database connection and management ----------------------------------
class DatabaseConnection:
    def __init__(self,table_name,tr_type,database,user,host,password,port):
        """
        Initializes the database connection.
        """
      
        self.conn = psycopg2.connect(
            database=database,
            user=user,
            host=host,
            password=password,
            port=port
        )
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        self.tr_type=tr_type
        self.column_list=["filename","Slicename"]
        for i in range(1,self.tr_type+1):
            self.column_list.append(f"Column_{i}")
        # print(self.column_list)


    def setup_table(self, table_name, tr_column):
        """
        Creates a table with the specified number of columns.
        """
        print("Under Set up table")
        # print(table_name, tr_column)
        # Generate the column definitions
        columns = [
            sql.SQL("{} TEXT").format(sql.Identifier("filename")),
            sql.SQL("{} TEXT").format(sql.Identifier("Slicename"))
        ] + [
            sql.SQL("{} TEXT").format(sql.Identifier(f"Column_{i}")) for i in range(1, tr_column + 1)
        ]

        # Combine column definitions into a single SQL object
        columns_str = sql.SQL(", ").join(columns)

        # Construct the CREATE TABLE query
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            columns_str
        )

        # Execute the query
        self.cursor.execute(query)
        self.conn.commit()


    def insert_data(self, filename, table_name, slice_name, data, tr_column):
        """
        Inserts or updates a row of data in the table.
        
        """
        print("Under Insert Data")
        # print("\n\n\n",data)
        # print(filename, table_name, slice_name, data, tr_column)

        if not isinstance(tr_column, int):
            raise ValueError("tr_column must be an integer representing the number of additional columns.")
        
        if len(data) != tr_column:
            raise ValueError(f"Expected {tr_column} data elements, but got {len(data)}.")

        # Check if slice_name exists
        check_query = sql.SQL("SELECT 1 FROM {} WHERE {} = %s").format(
            sql.Identifier(table_name),  # Ensures the table name is quoted
            sql.Identifier("Slicename") # Ensures the column name is quoted
        )
        self.cursor.execute(check_query, (slice_name,))
        exists = self.cursor.fetchone()

        print("-"*20,"Line 118")

        # if exists:
        #     # Update existing row
        #     print("-"*20,"Line 122")
        #     update_columns = [f"Column_{i} = %s" for i in range(1, tr_column + 1)]
        #     print(update_columns)
        #     update_query = sql.SQL(
        #         "UPDATE {} SET {}, filename = %s WHERE {} = %s"
        #         ).format(
        #             sql.Identifier(table_name),
        #             sql.SQL(", ").join(
        #                 sql.SQL("{} = %s").format(sql.Identifier(column)) for column in update_columns
        #             ),
        #             sql.Identifier("Test45_correction.Slicename")  # Properly quoting Slicename
        #     )

        #     self.cursor.execute(update_query, data + [filename, slice_name])
        #     print(f"Updated row for Slicename: {slice_name}")
       
        if exists:
            # Update existing row
            print("-"*20, "Line 122")
            update_columns = [f"Column_{i} = %s" for i in range(1, tr_column + 1)]
            print(update_columns)
            update_query = sql.SQL(
                "UPDATE {} SET {}, filename = %s WHERE {} = %s"
            ).format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(
                    sql.SQL("{} = %s").format(sql.Identifier(f"Column_{i}")) for i in range(1, tr_column + 1)
                ),
                sql.Identifier("Slicename")  # Correctly quoting Slicename
            )

            self.cursor.execute(update_query, data + [filename, slice_name])
            print(f"Updated row for Slicename: {slice_name}")

        else:
            # Insert new row
            print("-"*20,"Line 138")
            columns = ["filename", "Slicename"] + [f"Column_{i}" for i in range(1, tr_column + 1)]
            placeholders = ", ".join(["%s"] * len(columns))
            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(placeholders)
            )
            self.cursor.execute(insert_query, [filename, slice_name] + data)
            print(f"Inserted new row for slice_name: {slice_name}")
        
        self.conn.commit()

    def fetch_data(self, column, row_number, table_name):
        """
        Fetches data from the specified table and column at a given row.
        """
        print("under fetch _data code")
        try:
            # query = sql.SQL(f"SELECT {', '.join(self.column_list)} FROM {} OFFSET %s LIMIT 1").format(sql.Identifier(self.table_name))
            query = sql.SQL(
                            "SELECT {columns} FROM {table} OFFSET %s LIMIT 1"
                            ).format(
                            columns=sql.SQL(', ').join(map(sql.Identifier, self.column_list)),
                            table=sql.Identifier(self.table_name)
                        )

            self.cursor.execute(query, (row_number,))
            result = self.cursor.fetchone()
            # print(result)
            return result
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
            return None

    def close(self):
        """
        Closes the database connection.
        """
        self.cursor.close()
        self.conn.close()


# -------------------------- Utility: Counting images in a folder ---------------------------------
def count_images_in_folder(folder_path):
    image_extensions = {'.jpg', '.jpeg', '.png'}
    return sum(
        1 for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in image_extensions
    )

@app.route("/home/", methods=["POST"])
def home():
    print("Under home api")
    try:
        data = request.json
        img_folder_path = data.get("image_folder")
        table_name = data.get("table_name")
        new_table_name = data.get("new_table_name")
        cordinate_path = data.get("cordinate_file")
        tr_type = int(data.get("tr_type"))
        database=data.get("database")
        user=data.get("user")
        host=data.get("host")
        password=data.get("password")
        port=data.get("port")
        img_no=0
        col_no=0

        # if not all([img_folder_path, table_name, new_table_name, cordinate_path, tr_type, correct_data]):
        if not (img_folder_path and  database and user and host and password and port and cordinate_path and tr_type):
            return jsonify({"message": "Missing required data."}), 400

        # Mapping for total columns based on transformation type
        # {52: 47, 57: 52, 44: 38, 45: 38, 35: 29, 50: 44}
        total_col_map = {52: 52, 57: 57, 44: 44, 45: 45, 35: 35, 50: 50}
        total_col = total_col_map.get(tr_type, 0)

        if total_col == 0:
            return jsonify({"message": f"Invalid transformation type: {tr_type}."}), 400

        # Setup database
        db = DatabaseConnection( table_name,tr_type,database,user,host,password,port)
        db.setup_table(new_table_name, total_col)
         
        # Database operations
        
        img_name_row = db.fetch_data("slice_name", img_no,new_table_name)
        print("*"*26)
        print(img_name_row)
        if not img_name_row:
            return jsonify({"message": "No image found at the specified index."}), 404

        file_name=img_name_row[0]
        img_name = img_name_row[1]
        print(file_name,img_name)
        excel_data_row = db.fetch_data(f"Column_{col_no + 1}", img_no,new_table_name)
        print(excel_data_row)

        if not excel_data_row or len(excel_data_row) < 3:
            return jsonify({"message": "Data for the specified row or column is invalid."}), 404

        excel_data_row = excel_data_row[2:]
        img_path = os.path.join(img_folder_path, img_name)

        

        # Encode image in base64
        if not os.path.exists(img_path):
            return jsonify({"message": f"Image {img_name} not found."}), 404

        with open(img_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Decode coordinates
        with open(cordinate_path, "r") as f:
            coord_data = f.read().replace("'", "\"")
        try:
            parsed_data = json.loads(coord_data)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return jsonify({"message": "Error decoding JSON."}), 400

        cropped_slices_list = []
        # print(len(parsed_data["45"]))
        # print(parsed_data)
      
        for i in parsed_data.values():
          
            # print(i)
            for j in i:
         
                left = int(j.get("left"))
                top = int(j.get("top"))
                width = int(j.get("width")) if j.get("width") is not None else 80 
                height = int(j.get("height")) if j.get("height") is not None else 80

                

                img = cv2.imread(img_path)
                
                # if top + height > img.shape[0] or left + width > img.shape[1]:
                #     print(left,top,width,height,img.shape)
                #     return jsonify({"message":"Check the coordinates correctly in the annotation file"})

                cropped_image = img[top:top + height, left:left + width]
                success, buffer = cv2.imencode('.jpg', cropped_image)
                if success:
                   
                    col_slices = base64.b64encode(buffer).decode('utf-8')
                    cropped_slices_list.append(col_slices)
                else:
                    return jsonify({"message": "Failed to encode the image."}), 500
        print("-------------outside of for loop line 211")
        return jsonify({
            "image": image_base64,
            "col_slices": cropped_slices_list,
            "data": excel_data_row
        })

    except Exception as e:
        logger.error(f"Error in /correction/: {e}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

def reduce_slice_value(filename):
    # Use regex to find the slice number
    match = re.search(r'_slice_(\d+)', filename)
    if match:
        slice_number = int(match.group(1))
        new_slice_number = slice_number - 1
        new_filename = re.sub(r'_slice_\d+', f'_slice_{new_slice_number}', filename)
        return new_filename
    return filename  # Return the original filename if no match is found

# ----------------------------- Routes -------------------------------------------------------------
@app.route("/correction/", methods=["POST"])
def move_slices():
    print("Under correction api")
    try:
        data = request.json
        img_folder_path = data.get("image_folder")
        table_name = data.get("table_name")
        new_table_name = data.get("new_table_name")
        cordinate_path = data.get("cordinate_file")
        tr_type = int(data.get("tr_type"))
        img_no = int(data.get("img_number", 0))
        col_no = int(data.get("col_no", 1))
        correct_data = data.get("correct_data")
        database=data.get("database")
        user=data.get("user")
        host=data.get("host")
        password=data.get("password")
        port=data.get("port")

        img_no-=1

        # if not all([img_folder_path, table_name, new_table_name, cordinate_path, tr_type, correct_data]):
    
        if not (img_folder_path  and database and user and host and password and port and cordinate_path and tr_type and img_no >= 0 and col_no >= 0 and correct_data):
            return jsonify({"message": "Missing required data."}), 400

        # Mapping for total columns based on transformation type
        total_col_map = {52: 52, 57: 57, 44: 44, 45: 45, 35: 35, 50: 50}
        total_col = total_col_map.get(tr_type, 0)

        if total_col == 0:
            return jsonify({"message": f"Invalid transformation type: {tr_type}."}), 400

        # Database operations
        db = DatabaseConnection( table_name,tr_type,database,user,host,password,port)
        img_name_row = db.fetch_data("slice_name", img_no,new_table_name)
        file_name=img_name_row[0]

        print("-"*30,"Line 310")
        
        img_name_row=img_name_row[1]
       
        if not img_name_row:
            return jsonify({"message": "No image found at the specified index."}), 404

        
        img_name = img_name_row
        excel_data_row = db.fetch_data(f"Column_{col_no + 1}", img_no,new_table_name)

        if not excel_data_row or len(excel_data_row) < 3:
            return jsonify({"message": "Data for the specified row or column is invalid."}), 404

        excel_data_row = excel_data_row[2:]
        insertion_img_name=reduce_slice_value(img_name)
        img_path = os.path.join(img_folder_path, img_name)
      

        # Setup database
        db.setup_table(new_table_name, total_col)
        print("-"*50,"line 369")

        # Insert data into the database (update specific cell)
      
        db.insert_data(file_name, new_table_name, insertion_img_name,correct_data, total_col)
        db.close()
        print("-"*50,"line 374")

        # Encode image in base64
        if not os.path.exists(img_path):
            return jsonify({"message": f"Image {img_name} not found."}), 404

        with open(img_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Decode coordinates
        with open(cordinate_path, "r") as f:
            coord_data = f.read().replace("'", "\"")
        try:
            parsed_data = json.loads(coord_data)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return jsonify({"message": "Error decoding JSON."}), 400

        cropped_slices_list = []
        for i in parsed_data.values():
            for j in i:
                left = int(j.get("left"))
                top = int(j.get("top"))
                width = int(j.get("width"))
                height = int(j.get("height"))
                img = cv2.imread(img_path)

                # if top + height > img.shape[0] or left + width > img.shape[1]:
                #     return jsonify({"message":"Check the coordinates correctly in the annotation file"})

                cropped_image = img[top:top + height, left:left + width]
                success, buffer = cv2.imencode('.jpg', cropped_image)
                if success:
                    col_slices = base64.b64encode(buffer).decode('utf-8')
                    cropped_slices_list.append(col_slices)
                else:
                    return jsonify({"message": "Failed to encode the image."}), 500

        return jsonify({
            "image": image_base64,
            "col_slices": cropped_slices_list,
            "data": excel_data_row,
            "message": "Data has been inserted"
        })

    except Exception as e:
        logger.error(f"Error in /correction/: {e}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# ----------------------------- Routes -------------------------------------------------------------
@app.route("/previous/", methods=["POST"])
def previous():
    print("Under previous API")
    try:
        data = request.json
        img_folder_path = data.get("image_folder")
        table_name = data.get("table_name")
        new_table_name = data.get("new_table_name")
        cordinate_path = data.get("cordinate_file")
        tr_type = int(data.get("tr_type"))
        img_no = int(data.get("img_number", 0))
        col_no = int(data.get("col_no", 1))
        correct_data = data.get("correct_data")
        database=data.get("database")
        user=data.get("user")
        host=data.get("host")
        password=data.get("password")
        port=data.get("port")

        if img_no<0:
            return jsonify({"Error": "There is no data in the database before this."})

        if not (img_folder_path  and database and user and host and password and port and cordinate_path and tr_type and img_no >= 0 and col_no >= 0 and correct_data):
            return jsonify({"message": "Missing required data."}), 400

        # Mapping for total columns based on transformation type
        total_col_map = {52: 52, 57: 57, 44: 44, 45: 45, 35: 35, 50: 50}
        total_col = total_col_map.get(tr_type, 0)

        if total_col == 0:
            return jsonify({"message": f"Invalid transformation type: {tr_type}."}), 400

        # Database operations
        db = DatabaseConnection(table_name,tr_type,database,user,host,password,port)

        # Update the current `img_no` data in the database
        img_name_row = db.fetch_data("slice_name", img_no, new_table_name)
        if not img_name_row:
            return jsonify({"message": "No image found at the specified index."}), 404

        file_name = img_name_row[0]
        insertion_img_name = img_name_row[1] if len(img_name_row) > 1 else None

        print(f"Storing data for image no {img_no}: {file_name}, {correct_data}")
        db.setup_table(new_table_name, total_col)
        db.insert_data(file_name, new_table_name, insertion_img_name, correct_data, total_col)

        # Move to the previous image
        img_no -= 1
        if img_no < 0:
            return jsonify({"message": "No previous images available."}), 404

        img_name_row = db.fetch_data("slice_name", img_no, new_table_name)
        if not img_name_row:
            return jsonify({"message": "No image found at the previous index."}), 404

        file_name = img_name_row[0]
        img_name = img_name_row[1]
        img_path = os.path.join(img_folder_path, img_name)

        excel_data_row = db.fetch_data(f"Column_{col_no + 1}", img_no, new_table_name)
        if not excel_data_row or len(excel_data_row) < 3:
            return jsonify({"message": "Data for the specified row or column is invalid."}), 404

        excel_data_row = excel_data_row[2:]
        db.close()

        # Encode image in base64
        if not os.path.exists(img_path):
            return jsonify({"message": f"Image {img_name} not found."}), 404

        with open(img_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Decode coordinates
        with open(cordinate_path, "r") as f:
            coord_data = f.read().replace("'", "\"")
        try:
            parsed_data = json.loads(coord_data)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return jsonify({"message": "Error decoding JSON."}), 400

        cropped_slices_list = []
        for i in parsed_data.values():
            for j in i:
                left = int(j.get("left"))
                top = int(j.get("top"))
                width = int(j.get("width"))
                height = int(j.get("height"))

                # if top + height > img.shape[0] or left + width > img.shape[1]:
                #     return jsonify({"message":"Check the coordinates correctly in the annotation file"})

                img = cv2.imread(img_path)
                cropped_image = img[top:top + height, left:left + width]
                success, buffer = cv2.imencode('.jpg', cropped_image)
                if success:
                    col_slices = base64.b64encode(buffer).decode('utf-8')
                    cropped_slices_list.append(col_slices)
                else:
                    return jsonify({"message": "Failed to encode the image."}), 500

        return jsonify({
            "image": image_base64,
            "col_slices": cropped_slices_list,
            "data": excel_data_row,
            "message": "Data has been inserted"
        })

    except Exception as e:
        logger.error(f"Error in /previous/: {e}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)