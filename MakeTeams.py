import sys
import unittest
import csv
import math
import random

random.seed(1868)

class Team():
    def __init__(self, number):
        self.members = []
        self.oldMembers = []
        self.number = number

    def getGpa(self):
        return (float(sum(map((lambda student: student.gpa), self.oldMembers))) / 
                len(self.oldMembers))

    def __str__(self):
        returnString = 'Team ' + str(self.number + 1) + '\t' + str(round(self.getGpa(), 3)) + '\n'
        
        for OldMember in self.oldMembers:
            returnString += str(OldMember) + '\n'

        for member in self.members:
            returnString += str(member) + '\n'

        return returnString

class Member():
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def __str__(self):
        return self.firstName + ' ' + self.lastName

    def __eq__(self, other):
        return self.firstName == other.firstName and self.lastName == other.lastName


class OldMember(Member):
    def __init__(self, firstName, lastName, gpa):
        Member.__init__(self, firstName, lastName)
        self.gpa = gpa


def parseoldMembers(fileName):
    members = []

    with open(fileName, 'rb') as file:
        reader = csv.reader(file)

        for row in reader:
                members.append(OldMember(row[0].strip(), 
                                       row[1].strip(), 
                                       float(row[2].strip())))

    return members

def parseMembers(fileName):
    members = []

    with open(fileName, 'rb') as file:
        reader = csv.reader(file)

        for row in reader:
            members.append(Member(row[0].strip(),
                                  row[1].strip()))
            
    return members

membersFile = 'New Members.csv'
oldMembersFile = 'Copy of Spring 2017 Grades - Grades.csv'

oldMembers = parseoldMembers(oldMembersFile)
members = parseMembers(membersFile)

oldMembers.sort(key=lambda x: -x.gpa)

teamNumber = 0

teamPike = Team(teamNumber)
teamPike.members = members
teamPike.oldMembers = oldMembers

chapterAverage = teamPike.getGpa()

def calcVariance(team, chapterAverage):
    return (team.getGpa() - chapterAverage)**2

def swapMembers(firstTeam, firstIndex, secondTeam, secondIndex):
    firstMember = firstTeam.oldMembers.pop(firstIndex)
    secondMember = secondTeam.oldMembers.pop(secondIndex)

    firstTeam.oldMembers.append(secondMember)
    secondTeam.oldMembers.append(firstMember)

def undoSwap(firstTeam, secondTeam):
    firstMember = firstTeam.oldMembers.pop()
    secondMember = secondTeam.oldMembers.pop()

    firstTeam.oldMembers.append(secondMember)
    secondTeam.oldMembers.append(firstMember)

numTeams = 25
teams = []

for i in range(numTeams):
    teams.append(Team(i))

for i in range(len(oldMembers)):
    teams[i%numTeams].oldMembers.append(oldMembers[i])

firstTotVar = 0

for team in teams:
    print(team)
    firstTotVar += calcVariance(team, chapterAverage)

for i in range(10000):
    firstTeamIndex = int(math.floor(random.random()*numTeams))
    secondTeamIndex = int(math.floor(random.random()*numTeams))
    
    if(firstTeamIndex == secondTeamIndex):
        continue

    firstTeam = teams[firstTeamIndex]
    secondTeam = teams[secondTeamIndex]
    
    firstTeamMemberIndex = int(math.floor(random.random()*len(firstTeam.oldMembers)))
    secondTeamMemberIndex = int(math.floor(random.random()*len(secondTeam.oldMembers)))
    
    firstVariance = calcVariance(firstTeam, chapterAverage) + calcVariance(secondTeam, chapterAverage)
    
    swapMembers(firstTeam, firstTeamMemberIndex, secondTeam, secondTeamMemberIndex)
    
    secondVariance = calcVariance(firstTeam, chapterAverage) + calcVariance(secondTeam, chapterAverage)
    
    if firstVariance < secondVariance:
        undoSwap(firstTeam, secondTeam)

print('\n\nAfter fudging the numbers...\n')

secondTotVar = 0

for i in range(len(oldMembers), (len(members) + len(oldMembers))):
    teams[i%numTeams].members.append(members[i-len(oldMembers)])

for team in teams:
    print(team)
    secondTotVar += calcVariance(team, chapterAverage)

print('Before: ' + str(firstTotVar))
print('After: ' + str(secondTotVar))
