# DES model Open Code Checklist
This checklist is adapted from the [NHSE Repo Template](https://github.com/nhsengland/nhse-repository-template/blob/main/OPEN_CODE_CHECKLIST.md)
Please use this checklist to document adherence to best practice for published projects.

## When publishing your code you need to make sure:
  
### you’re clear about who owns the code and how others can use it

- [x] Does your code have an appropriate licence and copyright notice?  (**Mandatory**)
- [x] Is there a README and does it document intended purpose? (**Mandatory**)
- [x] Is the README clear and concise? (**Optional** - use analytics unit template or [example](https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md))
- [x] Do you need to consider MHRA 'software as a medical device' guidance? **No** (**Mandatory** - use [flowchart](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/999908/Software_flow_chart_Ed_1-08b-IVD.pdf))
- [x] Who has responsibility for ongoing support and communications for the code, including addressing any security concerns? **helenajr** (**Mandatory** Best practice to assign, else state the code is not maintained and when the last update was)
- [x] Are package dependencies and libaries documented with versions? (**Optional**)
- [x] Has the code been linked to any published outputs so others can easily link to the code? **No published outputs** (**Optional**) 

### You do not release information that should remain closed

- [x] Does the code include any sensitive, personal, secret or top secret data/information? **No** (**Mandatory**)
- [x] Does the code include any unreleased policy? **No** (**Mandatory**)
- [x] Does the code include business sensitive algorithms (e.g. finance allocations)? **No** (**Mandatory**)
- [x] Are the relevant stakeholders aware of this project? **Yes** (**Mandatory**)
- [x] Are any credentials contained in the source code or commits? **No** (**Mandatory** - check in both current version and git history)
- [x] Are any secret keys contained in the source code or commits? **No** (**Mandatory** - check in both current version and git history)
- [x] Are any SQL server addresses or connection strings in the source code or commits? **No** (**Mandatory** - check in both current version and git history)
- [x] Does the git history contain any sensitive information (e.g. at one time real data or credentials were in the code but have since been removed) **No** (**Mandatory**)
- [x] Have notebook outputs been removed/checked for sensitive information? **No notebooks** (**Mandatory** - check but some appropriate outputs maybe useful: [Example]( https://github.com/best-practice-and-impact/govcookiecutter/blob/main/%7B%7B%20cookiecutter.repo_name%20%7D%7D/.pre-commit-config.yaml))
- [x] have you checked any screenshots or figures in your outputs and documentation for information that shouldn't be released? (**Mandatory**)

### You store it in a repository managed by your department (to make licensing/copyright clear)

- [x] Is the code version controlled using GIT or similar? (**Optional**)
- [x] Is the code stored in your organisational GitHub account? (**Optional**)

### An internal code review has been completed

- [ ] Has a colleague reviewed the code for sensitive data content and security vulnerabilities? (**Mandatory** - Best practice is to record automated code quality and security tools used) **No, as considered very low risk**
- [ ] Has a code quality review been completed focussing on the end usability and clarity? (**Optional** - consider runing through the [example](https://best-practice-and-impact.github.io/qa-of-code-guidance/checklist_higher.html) or similar code quality checklist)
- [ ] Has the code undergone some level of testing.  The level of teting required will depend on the specific code and use-case but as minimum it should work in a fresh environment with arteficial data. (**Optional**)

