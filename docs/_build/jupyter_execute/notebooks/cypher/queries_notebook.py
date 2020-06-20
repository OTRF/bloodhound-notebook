# Queries Notebook


* **Author**: Roberto Rodriguez (@Cyb3rWard0g)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
    

## Import Libraries

from py2neo import Graph

## Initialize Graph Variable

graph = Graph(password='wardog')

## Community Cypher Queries

## Servers a user can RDP into
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find servers a user can RDP into.


graph.run(
'''
MATCH p=(g:Group)-[:CanRDP]->(c:Computer)
WHERE  g.objectid ENDS WITH '-513' AND c.operatingsystem CONTAINS 'Server'
RETURN p   
'''
).data()

## View all GPOs that contain a keyword
**Author:** Ryan Hausknecht (@haus3c)

**Description:** View all GPOs that contain a keyword


graph.run(
'''
MATCH (n:GPO)
WHERE n.name CONTAINS "DOMAIN"
RETURN n
'''
).data()

## Domain Users Groups with Interesting ACEs
**Author:** Ryan Hausknecht (@haus3c), Roberto Rodriguez (@Cyb3rWard0g)

**Description:** Find interesting privileges/ACEs that have been configured to DOMAIN USERS group


graph.run(
'''
MATCH (m:Group)
WHERE m.name =~ 'DOMAIN USERS@CONTOSO.LOCAL'
MATCH p=(m)-[r:Owns|WriteDacl|GenericAll|WriteOwner|ExecuteDCOM|GenericWrite|AllowedToDelegate|ForceChangePassword]->(n:Computer)
RETURN p
'''
).data()

## Top 10 Computers with Most Admins
**Author:** Walter.Legowski (@SadProcessor)

**Description:** List of top 10 computers with most admins


graph.run(
'''
MATCH (n:User),(m:Computer),(n)-[r:AdminTo]->(m)
WHERE NOT n.name STARTS WITH 'ANONYMOUS LOGON' AND NOT n.name='' WITH m,count(r) as rel_count 
ORDER BY rel_count desc 
LIMIT 10 
MATCH (m)<-[r:AdminTo]-(n) 
RETURN n,r,m
'''
).data()

## Map Domain Trusts
**Author:** Walter.Legowski (@SadProcessor)

**Description:** Map domain trusts


graph.run(
'''
MATCH (n:Domain) MATCH p=(n)-[r]-() RETURN p
'''
).data()

## High Value Target Group
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Show all high value target group


graph.run(
'''
MATCH p=(n:User)-[r:MemberOf*1..]->(m:Group {highvalue:true})
RETURN p
'''
).data()

## Shortest Path to DA Groups from Domain Users Groups
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Shortest paths to Domain Admins group from the Domain Users group


graph.run(
'''
MATCH (g:Group)
WHERE g.name =~ 'DOMAIN USERS@.*'
MATCH (g1:Group)
WHERE g1.name =~ 'DOMAIN ADMINS@.*'
OPTIONAL MATCH p=shortestPath((g)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(g1))
RETURN p
'''
).data()

## ASP-REQ Roastable Users
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find user that doesn’t require kerberos pre-authentication (aka AS-REP Roasting)


graph.run(
'''
MATCH (u:User {dontreqpreauth: true})
RETURN u
'''
).data()

## Unprivileged Users with Rights to Add Members to Groups
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find if unprivileged users have rights to add members into groups


graph.run(
'''
MATCH (n:User {admincount:False})
MATCH p=allShortestPaths((n)-[r:AddMember*1..]->(m:Group))
RETURN p
'''
).data()

## Users that Logged in ithin Threshold
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find users that logged in within the last 90 days. Change 90 to whatever threshold you want.


graph.run(
'''
MATCH (u:User)
WHERE u.lastlogon < (datetime().epochseconds - (90 * 86400)) and NOT u.lastlogon IN [-1.0, 0.0]
RETURN u.name
'''
).data()

## Shortest Path to DA Groups from Non-Privileged Domain Users
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Shortest paths to Domain Admins group from non privileged users (AdminCount=false)


graph.run(
'''
MATCH (n:User {admincount:false}),(m:Group {name:'DOMAIN ADMINS@CONTOSO.LOCAL'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m))
RETURN p
'''
).data()

## Unsupported OSs
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find unsupported OSs


graph.run(
'''
MATCH (H:Computer) WHERE H.operatingsystem =~ '.*(2000|2003|2008|xp|vista|7|me)*.'
RETURN H.name
'''
).data()

## Top 10 Users with Most Sessions
**Author:** Walter.Legowski (@SadProcessor)

**Description:** List Top 10 Users with Most Sessions


graph.run(
'''
MATCH (n:User),(m:Computer),(n)<-[r:HasSession]-(m) 
WHERE NOT n.name STARTS WITH 'ANONYMOUS LOGON' 
AND NOT n.name='' WITH n, 
count(r) as rel_count 
order by rel_count desc 
LIMIT 10 
MATCH (m)-[r:HasSession]->(n) 
RETURN n,r,m
'''
).data()

## Users with Passwords Last Set withing Threshold
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find users with passwords last set thin the last 90 days. Change 90 to whatever threshold you want.


graph.run(
'''
MATCH (u:User)
WHERE u.lastlogon < (datetime().epochseconds - (90 * 86400)) and NOT u.lastlogon IN [-1.0, 0.0]
RETURN u.name
'''
).data()

## Shortest Path to DA Groups from Computers
**Author:** Ryan Hausknecht (@haus3c), Roberto Rodriguez (@Cyb3rWard0g)

**Description:** Shortest paths to Domain Admins group from computers


graph.run(
'''
MATCH (n:Computer),(m:Group {name:'DOMAIN ADMINS@CONTOSO.LOCAL'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m))
RETURN p
'''
).data()

## All Domain Users CanRDP Edges Against all Computers
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find only the CanRDP privileges (edges) of the domain users against the domain computers


graph.run(
'''
MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group)))
MATCH p2=(u1)-[:CanRDP*1..]->(c:Computer)
RETURN p2
'''
).data()

## All Domain Users AdminTo Edges Against all Computers
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find only the AdminTo privileges (edges) of the domain users against the domain computers


graph.run(
'''
MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group)))
MATCH p2=(u1)-[:AdminTo*1..]->(c:Computer)
RETURN p2
'''
).data()

## Active Users Sessions in all Domain Computers
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find the active user sessions on all domain computers


graph.run(
'''
MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group)))
MATCH p2=(c:Computer)-[*1]->(u1)
RETURN p2
'''
).data()

## Kerberoastable Users with a path to DA
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find Kerberoastable Users with a path to DA


graph.run(
'''
MATCH (u:User {hasspn:true})
MATCH (g:Group)
WHERE g.name CONTAINS 'DOMAIN ADMINS' MATCH p = shortestPath( (u)-[*1..]->(g) )
RETURN p
'''
).data()

## Kerberoastable Users
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find All Users with an SPN/Find all Kerberoastable Users


graph.run(
'''
MATCH (n:User)WHERE n.hasspn=true
RETURN n.name
'''
).data()

## Specific Users Edges to All Nodes
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find all Edges that a specific user has against all the nodes (HasSession is not calculated, as it is an edge that comes from computer to user, not from user to computer)


graph.run(
'''
MATCH (n:User)
WHERE n.name =~ 'JEFFMCJUNKIN@CONTOSO.LOCAL'
MATCH (m)
WHERE NOT m.name = n.name
MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m))
RETURN p
LIMIT 10
'''
).data()

## Shortest Path to DA Groups from Domain Groups
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Shortest paths to Domain Admins group from all domain groups


graph.run(
'''
MATCH (n:Group)
WHERE NOT n.name = 'DOMAIN ADMINS@CONTOSO.LOCAL'
MATCH (m:Group {name:'DOMAIN ADMINS@CONTOSO.LOCAL'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m))
RETURN p
'''
).data()

## Shortest Path to DA Groups from Non-Privileged Domain Groups
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Shortest paths to Domain Admins group from non-privileged groups (AdminCount=false)


graph.run(
'''
MATCH (n:Group {admincount:false}),(m:Group {name:'DOMAIN ADMINS@CONTOSO.LOCAL'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m))
RETURN p
'''
).data()

## Shortest Path to DA Groups from Computers Excluding DCs
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Shortest paths to Domain Admins group from computers excluding potential DCs (based on ldap/ and GC/ spns)


graph.run(
'''
WITH '(?i)ldap/.*' as regex_one WITH '(?i)gc/.*' as regex_two
MATCH (n:Computer)
WHERE NOT ANY(item IN n.serviceprincipalnames WHERE item =~ regex_two OR item =~ regex_two )
MATCH(m:Group {name:"DOMAIN ADMINS@CONTOSO.LOCAL"}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m))
RETURN p
'''
).data()

## Unprivileged Users Edges to All Nodes
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find all the Edges that any UNPRIVILEGED user (based on the admincount:False) has against all the nodes


graph.run(
'''
MATCH (n:User {admincount:False})
MATCH (m)
WHERE NOT m.name = n.name
MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m))
RETURN p
LIMIT 10
'''
).data()

## Unprivileged Users ACL abusing other Users
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find interesting edges related to “ACL Abuse” that uprivileged users have against other users


graph.run(
'''
MATCH (n:User {admincount:False})
MATCH (m:User)
WHERE NOT m.name = n.name
MATCH p=allShortestPaths((n)-[r:AllExtendedRights|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner*1..]->(m))
RETURN p
'''
).data()

## Workstations a user can RDP into
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find workstations a user can RDP into.


graph.run(
'''
MATCH p=(g:Group)-[:CanRDP]->(c:Computer)
WHERE g.objectid ENDS WITH '-513' AND NOT c.operatingsystem CONTAINS 'Server'
RETURN p
'''
).data()

## All Domain Users Edges Against all Computers
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find all the privileges (edges) of the domain users against the domain computers (e.g. CanRDP, AdminTo etc. HasSession edge is not included)


graph.run(
'''
MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group)))
MATCH p2=(u1)-[*1]->(c:Computer)
RETURN p2
'''
).data()

## All Logged In Admins
**Author:** Walter.Legowski (@SadProcessor)

**Description:** List of all logged in administrators


graph.run(
'''
MATCH 
p=(a:Computer)-[r:HasSession]->(b:User) 
WITH a,b,r 
MATCH 
p=shortestPath((b)-[:AdminTo|MemberOf*1..]->(a)) 
RETURN b,a,r
'''
).data()

## All Domain Admins
**Author:** Walter.Legowski (@SadProcessor)

**Description:** List of all domain admins


graph.run(
'''
MATCH (n:Group) WHERE n.name =~ "(?i).*DOMAIN ADMINS.*"
WITH n 
MATCH (n)<-[r:MemberOf*1..]-(m) 
RETURN n,r,m
'''
).data()

## Computers with Unconstrained Delegation
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find all computers with Unconstrained Delegation


graph.run(
'''
MATCH (c:Computer {unconstraineddelegation:true})
RETURN c
'''
).data()

## Unprivileged Users ACL abusing Computers
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find interesting edges related to “ACL Abuse” that unprivileged users have against computers


graph.run(
'''
MATCH (n:User {admincount:False})
MATCH p=allShortestPaths((n)-[r:AllExtendedRights|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|AdminTo|CanRDP|ExecuteDCOM|ForceChangePassword*1..]->(m:Computer))
RETURN p
'''
).data()

## User Sessions in a Specific Domain
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find all sessions any user in a specific domain has.


graph.run(
'''
MATCH p=(m:Computer)-[r:HasSession]->(n:User {domain: "CONTOSO.LOCAL"})
RETURN p
'''
).data()

## Top 10 Users with Most Local Admin Rights
**Author:** Walter.Legowski (@SadProcessor)

**Description:** List of top 10 users with most local admin rights


graph.run(
'''
MATCH (n:User),(m:Computer),(n)-[r:AdminTo]->(m)
WHERE NOT n.name STARTS WITH 'ANONYMOUS LOGON' AND NOT n.name='' WITH n, count(r) as rel_count
ORDER BY rel_count desc 
LIMIT 10 
MATCH (m)<-[r:AdminTo]-(n) 
RETURN n,r,m 
'''
).data()

## View all GPOs
**Author:** Ryan Hausknecht (@haus3c)

**Description:** View all GPOs


graph.run(
'''
MATCH (n:GPO)
RETURN n
'''
).data()

## SPNs with keywords
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find SPNs with keywords (swap SQL with whatever)


graph.run(
'''
MATCH (u:User)
WHERE ANY (x IN u.serviceprincipalnames WHERE toUpper(x) CONTAINS 'SQL')
RETURN u.name
'''
).data()

## Group with keywords
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find a group with keywords. E.g. SQL ADMINS or SQL 2017 ADMINS


graph.run(
'''
MATCH (g:Group)
WHERE g.name =~ '(?i).SQL.ADMIN.*'
RETURN g
'''
).data()

## Kerberoastable Users with passwords last set > 5 years
**Author:** Ryan Hausknecht (@haus3c)

**Description:** Find All Users with an SPN/Find all Kerberoastable Users with passwords last set > 5 years ago


graph.run(
'''
MATCH (u:User)
WHERE u.hasspn=true AND u.pwdlastset < (datetime().epochseconds - (1825 * 86400)) AND NOT u.pwdlastset IN [-1.0, 0.0]
RETURN u.name, u.pwdlastset order by u.pwdlastset
'''
).data()

## DA sessions not on a certain group
**Author:** Ryan Hausknecht (@haus3c)

**Description:** DA sessions not on a certain group (e.g. domain controllers).


graph.run(
'''
OPTIONAL MATCH (c:Computer)-[:MemberOf]->(t:Group)
WHERE NOT t.name = 'DOMAIN CONTROLLERS@CONTOSO.LOCAL' WITH c as NonDC
MATCH p=(NonDC)-[:HasSession]->(n:User)-[:MemberOf]->(g:Group {name:'DOMAIN ADMINS@CONTOSO.LOCAL'})
RETURN DISTINCT (n.name) as Username, COUNT(DISTINCT(NonDC)) as Connexions
ORDER BY COUNT(DISTINCT(NonDC)) DESC   
'''
).data()