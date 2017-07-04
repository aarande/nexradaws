Tutorial
########

The first step when working with nexradaws is to instantiate an instance of the NexradAwsInterface class.
This will create all the necessary connections to the NEXRAD Amazon S3 bucket.

.. code-block:: python

    import nexradaws
    conn = nexradaws.NexradAwsInterface()

Once we have this we can use the methods available in the :class:`NexradAwsInterface <nexradaws.NexradAwsInterface>`
object to make queries for metadata and for available NEXRAD files.

First let's see what years are available in the AWS bucket.

.. code-block:: python

    years = conn.get_avail_years()

