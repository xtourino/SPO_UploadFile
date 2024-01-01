# Import the necessary libraries
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def get_sharepoint_context(client_id, client_secret, tenant_prefix):
    """
    Function to get SharePoint context.
    :param client_id: Client ID for SharePoint
    :param client_secret: Client Secret for SharePoint
    :param tenant_prefix: Tenant prefix for SharePoint URL
    :return: ClientContext object
    """
    try:
        logging.info('Getting SharePoint context...')
        sharepoint_url = f'https://{tenant_prefix}.sharepoint.com'
        client_credentials = ClientCredential(client_id, client_secret)
        ctx = ClientContext(sharepoint_url).with_credentials(client_credentials)
        logging.debug('SharePoint context obtained.')
        return ctx
    except Exception as e:
        logging.error(f"Error getting SharePoint context: {e}")
        return None


def upload_file_to_sharepoint(ctx, local_file_path, sharepoint_folder_url):
    """
    Function to upload file to SharePoint.
    :param ctx: ClientContext object
    :param local_file_path: Local path of the file to be uploaded
    :param sharepoint_folder_url: SharePoint folder URL where file will be uploaded
    """
    try:
        logging.info(f'Uploading file {local_file_path} to SharePoint...')
        with open(local_file_path, 'rb') as content_file:
            file_content = content_file.read()
        target_file = os.path.join(sharepoint_folder_url, os.path.basename(local_file_path))
        File.save_binary_direct(ctx, target_file, file_content)
        logging.info(f"File uploaded to {target_file}")
    except Exception as e:
        logging.error(f"Error uploading file: {e}")


def main():
    """
    Main function to call other functions
    """
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Upload a file to SharePoint.')
    parser.add_argument('--client_id', required=True, help='Client ID for SharePoint')
    parser.add_argument('--client_secret', required=True, help='Client Secret for SharePoint')
    parser.add_argument('--tenant_prefix', required=True, help='Tenant prefix for SharePoint URL')
    parser.add_argument('--local_file_path', required=True, help='Local path of the file to be uploaded')
    parser.add_argument('--sharepoint_folder_url', required=True,
                        help='SharePoint folder URL where file will be uploaded')
    args = parser.parse_args()

    # Get the SharePoint context
    ctx = get_sharepoint_context(args.client_id, args.client_secret, args.tenant_prefix)
    if ctx is not None:
        # Upload the file to SharePoint
        upload_file_to_sharepoint(ctx, args.local_file_path, args.sharepoint_folder_url)
    else:
        logging.error("Unable to get SharePoint context. Exiting...")


# Call the main function
if __name__ == "__main__":
    main()
