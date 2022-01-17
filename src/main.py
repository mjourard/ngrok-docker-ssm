import logging
import boto3
import env
import ssm_tunnel_manager
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Creates or removed saved ssm parameters of active ngrok tunnels')
    parser.add_argument('action', type=str,
                        choices=['save', 'delete'], )
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')
    global myEnv
    myEnv = env.Config()
    myEnv.get(myEnv.ENV_NGROK_BASE_AGENT_URL)
    ngrok_agent_base_url = myEnv.get(myEnv.ENV_NGROK_BASE_AGENT_URL)
    ssm_prefix = myEnv.get(myEnv.ENV_SSM_PREFIX)
    aws_region = myEnv.get(myEnv.ENV_AWS_DEFAULT_REGION)
    ssm = boto3.client('ssm',
                       region_name=aws_region
                       )
    manager = ssm_tunnel_manager.Client(ssm, ssm_prefix, ngrok_agent_base_url)

    tunnels = manager.get_tunnels()
    if len(tunnels) == 0:
        logging.error(
            f"No ngrok tunnels found with a name and HTTPS protocol at {ngrok_agent_base_url}. Please make sure ngrok is running and accessible from that address.")
        exit(1)

    logging.info(f'Found {len(tunnels)} tunnel(s) to save to SSM...')

    args = vars(parse_arguments())
    print(args)
    if not 'action' in args:
        logging.error(f'shit is broke')
        exit(1)

    action = args['action']
    if action == 'save':
        manager.save_tunnels_in_ssm(tunnels)
    elif action == 'delete':
        manager.remove_tunnels_from_ssm(tunnels)
    else:
        logging.error(f'Unexpected action found: {action}')


if __name__ == '__main__':

    main()
