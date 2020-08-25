# aws-tool

This package provides a command line interface to for federation or AMS AWS users.

### Installation

The safest way to install the AWS CLI is to use [pip](https://pip.pypa.io/en/stable/) in a `virtualenv`:

    $ python -m pip install awstool

or, if you are not installing in a `virtualenv`, to install globally:

    $ sudo python -m pip install awstool

or for your user:

    $ python -m pip install --user awstool

If you have the aws-tool package installed and want to upgrade to the latest version you can run:

    $ python -m pip install --upgrade awstool

This will install the aws-tool package as well as all dependencies.

### Configuration
Before using the AWS Tool, you need to configure your AWS credentials.

The quickest way to get started is to run the `awstool configure` command:

    $ awstool configure
    Enter your Identity Source Domain(like sso.example.com):sso.example.com
    Enter your Identity User(like user@example.com):Fake.User@example.com
    Enter your Identity Password:

### Basic Commands

An AWS Tool command has the following structure:

    $ awstool <command> <subcommand> [options and parameters]

For example, to generate credentials, the command would be:

    $ awstool credential --generate-account

*Note*

It's only necessary to run command with `--generate-account` when it's your first time running this command or
you are really want to re-generate account.
That's to say, `awstool credential` is ok for your subsequent use.
    
To view help documentation, use one of the following:

    $ awstool --help
    $ awstool <command> --help
    $ awstool <command> <subcommand> --help

To get the version of the AWS CLI:

    $ awstool --version

## Getting Help

The best way to interact with our team is through GitHub. You can [open an issue](https://github.com/zhan9san/aws-tool/issues/new/choose).

Please check for open similar [issues](https://github.com/zhan9san/aws-tool/issues) before opening another one.

The AWS Tool implements AWS service APIs. For general issues regarding the services or their limitations, you may find the [Amazon Web Services Discussion Forums](https://forums.aws.amazon.com/) helpful.

## More Resources

- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/index.html)
- [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [Amazon Web Services Discussion Forums](https://forums.aws.amazon.com/)
- [AWS Support](https://console.aws.amazon.com/support/home#/)
- [AMS Documentation](https://console.aws.amazon.com/managedservices/docs/index.html)