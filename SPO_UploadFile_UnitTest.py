import unittest
from unittest.mock import patch, MagicMock
from main import get_sharepoint_context, \
    upload_file_to_sharepoint  # replace 'main' with the name of your module


class TestSharePoint(unittest.TestCase):
    @patch('main.ClientCredential')
    @patch('main.ClientContext')
    def test_get_sharepoint_context(self, mock_client_context, mock_client_credential):
        # Arrange
        mock_client_credential.return_value = MagicMock()
        mock_client_context.return_value.with_credentials.return_value = MagicMock()
        client_id = 'client_id'
        client_secret = 'client_secret'
        tenant_prefix = 'tenant_prefix'

        # Act
        result = get_sharepoint_context(client_id, client_secret, tenant_prefix)

        # Assert
        self.assertIsNotNone(result)
        mock_client_credential.assert_called_once_with(client_id, client_secret)
        mock_client_context.assert_called_once_with(f'https://{tenant_prefix}.sharepoint.com')

    @patch('main.File')
    @patch('main.os.path')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'data')
    def test_upload_file_to_sharepoint(self, mock_open, mock_os_path, mock_file):
        # Arrange
        ctx = MagicMock()
        local_file_path = 'local_file_path'
        sharepoint_folder_url = 'sharepoint_folder_url'
        mock_os_path.basename.return_value = 'file_name'
        mock_os_path.join.return_value = 'target_file'

        # Act
        upload_file_to_sharepoint(ctx, local_file_path, sharepoint_folder_url)

        # Assert
        mock_open.assert_called_once_with(local_file_path, 'rb')
        # mock_os_path.basename.assert_called_once_with(local_file_path)
        mock_os_path.join.assert_called_once_with(sharepoint_folder_url, 'file_name')
        mock_file.save_binary_direct.assert_called_once_with(ctx, 'target_file', b'data')


if __name__ == '__main__':
    unittest.main()
