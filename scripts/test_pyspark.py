import os
import sys
import subprocess
import traceback

print('Python executable:', sys.executable)
# Set JAVA_HOME explicitly to the Homebrew path we installed earlier
java_home = '/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home'
if os.path.exists(java_home):
    os.environ['JAVA_HOME'] = java_home
    os.environ['PATH'] = java_home + '/bin:' + os.environ.get('PATH', '')
    print('Set JAVA_HOME to', java_home)
else:
    print('JAVA_HOME path not found:', java_home)

# show which java is picked up and its version
try:
    which_java = subprocess.check_output(['which', 'java']).decode().strip()
except Exception:
    which_java = 'which java failed'
print('which java ->', which_java)
try:
    java_ver = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode()
except Exception as e:
    java_ver = f'java -version failed: {e}'
print('java -version output:\n', java_ver)

# Attempt to import pyspark and create SparkSession
try:
    import pyspark
    from pyspark.sql import SparkSession
    print('pyspark version:', pyspark.__version__)
    spark = SparkSession.builder.master('local[*]').appName('mle_assignment1_test').getOrCreate()
    print('Created SparkSession, spark.version =', spark.version)
    df = spark.createDataFrame([(1, 'a'), (2, 'b')], ['id', 'val'])
    df.show()
    spark.stop()
    print('SparkSession stopped successfully')
except Exception:
    print('Exception when creating SparkSession:')
    traceback.print_exc()
    sys.exit(1)

print('Done')
