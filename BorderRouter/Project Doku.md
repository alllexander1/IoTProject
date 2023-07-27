![Sign in window](image.png)

After signing up, you have to put in your username and password and hit the log in button.

![aws academy navigation](image-1.png)

In the aws academy navigation you'll click on Modules and select Learner Lab.

![Learner Lab off](image-2.png)

In the Learner Lab environment click on the right side "Start Lab" and wait till the red button next to "AWS" on the left side turns green.

![Learner Lab on](image-3.png)

Click on "AWS" next to the green button and wait. If nothing happens, change your browser or check your ad blockers and settings.

![AWS Console Home](image-4.png)

![AWS Console Home search bar](image-5.png)

![AWS Console Home services search](image-6.png)

On your first visit, click on Services and scroll down to E. Choose EC2. A other option would be to write EC2 in the search bar and choose it from there. After visiting the EC2 (Instances (running)) Page you can also click on EC2 under Recently visited.

![EC2 Dashboard Resources](image-8.png)

Click on Instances (running)

![EC2 Dashboard Instances](image-9.png)

Click on the yellow "Launch instances" button on the right top corner.

![Launch an instance](image-11.png)

Give the instance a name

![Launch an instance](image-12.png)

Select a Amazon Machine Image (AMI). 
For our project we used ubuntu.
Click the ubuntu option. 
Leave the Server and the Architecture as it is.

![Launch an instance](image-13.png)

For the instance type, select the Free tier eligible version. Which is the t2.micro.

If you don't have a Key pair, click on "Create a new key pair" on the right side.
In the Window that will open, give the key pair a name.
Select RSA for the key pair type.
For the private file formate we used .pem so we could use OpenSSH.
If PuTTY is the preferred to use, choose .ppk
Click on the yellow button with the text "Create key pair" on it.
Choose a place to safe your key.
Choose the Key pair you created.

![Launch an instance](image-14.png)

Leave the Network Settings as they are.

![Launch an instance](image-15.png)

Set the configure storage to 30 GiB
Scroll down. Check the summary and click on the yellow button ("Launch instance") on the lower right corner.

The Instance will be shown under Instances after a little while. Under Status checked it might be shown as Initializing. After a while it will turn to 2/2 checks passed.

![Instances](image-17.png)

Click the checkbox next to the instance name.
In the lower part of the screen you will find the instance summary. 
Search for VPC ID and click on the ID.

![Your VPCs](image-18.png)

On this page, click again on the VPC ID.

![Used VPC](image-19.png)

Click on the "Actions" button on the upper right corner and choose "Edit CIDRs".

![Edit CIDRs](image-20.png)

Click on "Add new IPv6 CIDR

![Add IPv6 CIDR](image-21.png)

Select "Amazon-provided IPv6 CIDR block and click on "Select CIDR".

![Edit CIDRs](image-22.png)

You should now see the status "Associated".
Click on the VPC ID on the top to see details to your VPC ID. 

![VPC ID](image-23.png)

Here you should see your IPv6.
Click on Route tables on the left side navigation bar.

![Route tables](image-24.png)

In the lower part select the tier with the name "Routes" and click the button "Edit routes" on the right side.

![Edit routes](image-26.png)

Click "Add route" for the destination use ::/0 and for the target use your amazon default value. 
Click "Add route again and use the destination 0.0.0.0./0 if it is not already set. use the same default value as a target.
Save the changes with the click on the yellow button.
Click on "Route tables" at the top.

![Route tables](image-27.png)

Our new routes are now shown in the lower part.
Click on Subnets

![Subnets](image-28.png)

Click the checkbox next to the name. Click on the "Action" button on the upper right corner and select "Edit IPv6 CIDRs.

![Edit IPv6 CIDRs](image-29.png)

If the Subnet CIDR block is not already set, Click on "Add IPv6 CIDR" and save the changes by clicking the yellow button on the right lower corner.
Then go back to your instances screen.

![Instances](image-31.png)

![Instances](image-32.png)

Click the checkbox next to your instance and scroll further down on the lower part, till you see your Network interface click on the Interface ID.

![Network interface](image-33.png)

Click the Network Interface ID again.

![Network interface summary](image-34.png)

Click on the "Actions" button on the upper right corner and select "Manage IP addresses".

![Manage IP addresses](image-35.png)

Click the button "Assign new IP address" in the IPv6 section.

![IP addresses](image-36.png)

After clicking the Assign button, leave it to Auto-assign and click the yellow "Save" button.

![Network interface summary](image-37.png)

You wil end up at the Network interface summary page. Since your IPv6 addresses is not shown, click the page refreshing button.

![Network interface summary](image-38.png)

The IPv6 addresses should now be visible.
Go back to your instances screen.

![Instances](image-39.png)

Click the checkbox next to your instance. On the lower part, click on the tier "Security". Click the link under "Security groups".

![Security Groups](image-40.png)

On the lower part, stay on the tier "Inbound rules" and click the button on the right "Edit inbound rules.

![Edit inbound rules](image-41.png)

click on "Add rule".

![Edit inbound rules](image-42.png)

Fill in the list above. (Some ports could be different for you).
After filling in all of them, click the yellow button "Save rules".
Go back to your instances screen.

![Instances](image-43.png)

Click on the checkbox next to your instance and click the "Connect button". 

![Connect to instance](image-45.png)

On the first tier click on the yellow button "Connect".

![AWS Ubuntu Connect](image-44.png)

Now your instance is connected.
Go back to the Connect to instance screen.

![Connect to instance](image-46.png)

To be able to use multiple terminals of your instance, select the tier "SSH client". 
Copy the Example and use it in your Linux Ubuntu environment. To connect to your instance from a different terminal.

Your EC2 is established. 