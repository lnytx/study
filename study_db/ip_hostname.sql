/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50703
Source Host           : localhost:3306
Source Database       : get_sysinfo

Target Server Type    : MYSQL
Target Server Version : 50703
File Encoding         : 65001

Date: 2017-06-06 17:05:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `ip_hostname`
-- ----------------------------
DROP TABLE IF EXISTS `ip_hostname`;
CREATE TABLE `ip_hostname` (
  `ip` varchar(20) NOT NULL,
  `hostname` varchar(30) NOT NULL,
  `physicalCPU` varchar(4) DEFAULT NULL,
  `logicalCPU` varchar(4) DEFAULT NULL,
  `platform` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ip_hostname
-- ----------------------------
