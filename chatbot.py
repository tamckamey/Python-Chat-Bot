#!/usr/bin/python

import string;
#I apologize if this is not okay, but I am using dictonaries as well.

keywords = {
	'bluescreen' : 'bluescreen issues',
	'internet' : 'internet issues',
	'wifi' : 'internet issues',
	'power' : 'power issues',
	'turn on' : 'power issues',
	'turn back on' : 'power issues',
	'charge' : 'power issues',
	'ran into a problem' : 'bluescreen issues' #Putting this lower in the list since it is less specific. It refers to the bluescreen error message.
}

problems = {
	'power issues' : {"turn back on" : 0, "turn on" : 0, "power on" : 0, "black screen" : 0, "charge" : 0},
	'internet issues' : {"broken": 1, "slow": 1, "no internet" : 2, "no connection" : 2, "is out" : 2},
	'bluescreen issues' : {"blue screen" : 3, "bluescreen" : 3, "ran into a problem" : 3},
}

queries = [
 	#Power on
	{
		'reply' : "I'm sorry to hear that. Power issues are pretty common. Let's work this out together!",
		'solutions' : {
			#"PROMPT" : IfYes[[Say, Stop, requriesEscalation], IfNo[Say, Stop, requiresEscalation]]
			"Is the device plugged in?" : [["Plugged in but still no power? Let's continue.", False, False], ["That's likely the problem.\nPlug the device in and you should have power!", True, False]],
			"Do you see a charging light to indicate it is charging?" : [["The issue is likely the laptop itself.", True, True],["Luckily, it sounds like the issue is the power brick.", True, True]]
		}
	},
	#Slow Internet
	{
		'reply' : "A slow connection is never fun. Most times, the issue isn't the computer itself. Let's try to figure this out.",
		'solutions' : {
			#"PROMPT" : IfYes[[Say, Stop, requriesEscalation], IfNo[Say, Stop, requiresEscalation]]
			"To confirm the issue isn't the computer, let's restart it!\nOnce you've restarted your computer, is the problem solved?" : [["The issue must have been related to the driver. You should be good to go!", True, False], ["Hm. Perhaps the issue is the router itself.", False, False]],
			"To confirm the issue isn't the router or modem, let's restart it!\nOnce you've restarted your router and modem, is the problem solved?" : [["Wonderful! The issue must have been one of those devices. If this happens again, please contact your ISP.", True, False],["That's no good. The issue is possibly with your ISP. You should give them a call to continue!", True, True]]
		}
	},
	#Internet is Out
	{
		'reply' : "It's fortunate that you were able to reach out to me without internet! Let's see what we can do to fix this!",
		'solutions' : {
			#"PROMPT" : IfYes[[Say, Stop, requriesEscalation], IfNo[Say, Stop, requiresEscalation]]
			"Are you connected to the WiFi?" : [["Gotcha! Just wanted to check the basics to be safe! Let's keep going.", False, False], ["That's the issue! Connect to your WiFi and you'll be good to go!", True, False]],
			"To confirm the issue isn't the computer, let's restart it!\nOnce you've restarted your computer, is the problem solved?" : [["The issue must have been related to the driver. You should be good to go!", True, False], ["Hm. Perhaps the issue is the router itself.", False, False]],
			"To confirm the issue isn't the router or modem, let's restart it!\nOnce you've restarted your router and modem, is the problem solved?" : [["Wonderful! The issue must have been one of those devices. If this happens again, please contact your ISP.", True, False],["That's no good. The issue is possibly with your ISP. You should give them a call to continue!", True, True]]
		}
	},
	#BOSD
	{
		'reply' : "Oh, no. Those can be very scary. Don't worry, though. They're usually pretty easy to diagnose!",
		'solutions' : {
			#"PROMPT" : IfYes[[Say, Stop, requriesEscalation], IfNo[Say, Stop, requiresEscalation]]
			"Please visit our website and type in your error code. Do you see an answer?" : [["Often times, it's that simple! Please read the article and reach out if the problem persists!", True, False], ["Hm. We must have never heard of this error before!", True, True]],
		}
	}
]

escalationAlert = "This is outside of my ability. I've sent your email to one of our experts so they can further assist!";

def getYesOrNo(question):
	response = input("\n"+question+"\nYOUR REPLY: ")
	response = (("".join(x for x in response if not x in [",","'","."])).lower()); #This will remove apostrophes from reply and turn it lower case.
	affirmatives = {"it is", "yes", "yup", "yep", "it worked", "has worked", "yeah"}
	negatives = {"it isnt", "no", "nope", "didnt work", "hasnt worked"}
	for value in affirmatives:
		if value in response:
			return True;
	for value in negatives:
		if value in response:
			return False;
	return getYesOrNo("Don't worry. I'll wait while you check.\n\n"+question);

def getReply(response, tsPhase, tsPosition):
	response = ("".join(x for x in response if x != "'" and x != ",")).lower(); #This will remove apostrophes from reply and turn it lower case.
	if (tsPhase == 1):
		for k_i, k_v in keywords.items(): #Unless I missed it, the chapter on dictionaries didn't cover how to implement .Items. Just that it exists?
			if response.find(k_i) != -1:
				return getReply(response, 2, k_v);
		return getReply(input("Sorry, I don't understand. Could you please describe the issue again?\nYOUR REPLY: "), 1, 1);
	elif (tsPhase == 2):
		for p_i, p_v in problems[tsPosition].items():
			if response.find(p_i) != -1:
				return getReply(response, 3, p_v);
		return getReply(input("\nI'm sorry. I'm confused about what kind of "+tsPosition+" you are having.\nCan you try explaining it again to me?\n\nYOUR REPLY: "), 2, tsPosition);
	elif (tsPhase == 3):
			print("\n"+queries[tsPosition]['reply']);
			for s_i, s_v in queries[tsPosition]['solutions'].items():
				reply = getYesOrNo(s_i);
				if reply == True:
					if (s_v[0][1]):
						return s_v[0][0], s_v[0][2]
					else:
						print("\n"+s_v[0][0]+"\n");
				else:
					if (s_v[1][1]):
						return s_v[1][0], s_v[1][2]
					else:
						print("\n"+s_v[1][0]+"\n");



print("-Agent, Ophelia, has entered the chat-\n");
namePrompt = input("Thank you for contacting technical support; my name is Ophelia. I will be your laptop specialist today!\nTo begin, could I get your name?\n\nYOUR REPLY: ");
emailPrompt = input("\nThank you, "+namePrompt+"! In the event that we get disconnected, please provide your email to me.\n\nYOUR REPLY: ");
initialProblem = input("\nThank you! Could you describe the issue you're having with your Windows laptop?\n\nYOUR REPLY: ");

answer, needsEscalation = getReply(initialProblem, 1, 1);

print("\n"+answer+"\n");
if (needsEscalation):
	print(escalationAlert);
print("Thank you for contact technical support! Have a wonderful day!");
print("-Agent, Ophelia, has left the chat-");