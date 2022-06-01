## Building a recommender system using LightFM
### Tasks:
- Prepare data ok
- Built model ok
- evaluate model need more thing
- built web with model

#### making web form:
- form request
- get data from form
- return predict result
#### usefull:
```
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/quang-vn26/demo1.git
git push -u origin main
```

work with form:
```
from flask import request
var1 = request.form["datetime"]
```
save to csv file
```
df_questions_p.to_csv("demo.csv")
```

check the file and delete in python
```
def create_file_csv(my_var):
    my_var_name = [ k for k,v in locals().iteritems() if v == my_var][0]
    my_var_name+=".csv"
    if os.path.exists(my_var_name):
        os.remove(my_var_name)
    else:
        my_var.to_csv(my_var_name) 
```

load file the CSV to a html
```

```

big file in Github

```
git lfs install
git lfs track "*.csv"
git add .gitattributes
```