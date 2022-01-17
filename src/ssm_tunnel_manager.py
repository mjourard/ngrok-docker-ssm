
import requests
import logging
from requests.exceptions import HTTPError
from botocore.exceptions import ClientError


class Client():

    def __init__(self, ssm_client, ssm_prefix, ngrok_agent_base_url):
        """Initialize the client that interacts with ssm and ngrok
        :param ssm_client: base api URL of the locally running ngrok agent
        :type ssm_client: SSM.Client
        :param ssm_prefix: base api URL of the locally running ngrok agent
        :type ssm_prefix: str
        :param ngrok_agent_base_url: base api URL of the locally running ngrok agent
        :type ngrok_agent_base_url: str
        """
        self.ssm_client = ssm_client
        self.ssm_prefix = ssm_prefix
        self.ngrok_agent_base_url = ngrok_agent_base_url

    def get_tunnels(self):
        tunnels = []
        """Queries the ngrok agent url provided for active tunnels, parses the important values and returns them
        :return: A list of tunnel objects, consisting of a name and a public_url
        """
        tunnels_url = f'{self.ngrok_agent_base_url}/tunnels'
        try:
            response = requests.get(tunnels_url).json()['tunnels']
            for idx, tunnel in enumerate(response):
                logging.info(f"checking tunnel #{idx + 1}")
                name = None
                public_url = None
                usable_tunnel = False
                checked_proto = False
                for key, value in tunnel.items():
                    if key == "name":
                        name = value
                    elif key == "public_url":
                        public_url = value
                    elif key == "proto":
                        if value == "https":
                            usable_tunnel = True
                        checked_proto = True

                    if name and public_url and checked_proto:
                        break
                if name and public_url and usable_tunnel:
                    logging.info(
                        f"Found a usable tunnel to save: {name}: {public_url}")
                    tunnels.append({
                        'name': name,
                        'public_url': public_url
                    })
                else:
                    logging.info(f"Skipping tunnel #{idx+1}")

        except HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.error(f'Other error occurred: {err}')

        return tunnels

    def save_tunnels_in_ssm(self, tunnels):
        """Saves the passed in tunnels to ssm using the passed in ssm client. Parameter names will start with the ssm_prefix passed in
        :param tunnels: A list of tunnel objects to save in SSM
        :type tunnels: list
        :return: Return version of the parameter if successfully created else None
        """

        for tunnel in tunnels:
            param_name = f"{self.ssm_prefix}/{tunnel['name']}"
            param_value = tunnel['public_url']
            try:
                result = self.ssm_client.put_parameter(
                    Name=param_name,
                    Value=param_value,
                    Type='String',
                    Overwrite=True
                )
                logging.info(
                    f"Saved param {param_name} as version {result['Version']}")
            except ClientError as e:
                logging.error(e)
                return None

    def remove_tunnels_from_ssm(self, tunnels):
        """Deletes the ssm parameters that would exist for each of the tunnels passed in, according to the set ssm_prefix value
        :param tunnels: A list of tunnel objects to that map to SSM parameters and are going to be deleted.
        :type tunnels: list
        """
        for tunnel in tunnels:
            param_name = f"{self.ssm_prefix}/{tunnel['name']}"
            try:
                self.ssm_client.delete_parameter(
                    Name=param_name
                )
                logging.info(
                    f"Deleted param {param_name}")
            except ClientError as e:
                logging.error(e)
